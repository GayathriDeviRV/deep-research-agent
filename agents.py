import operator
from typing import TypedDict, List, Annotated
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import BaseMessage, HumanMessage
from llm_tools import llm, tavily_tool
from state import AgentState

# --- Researcher Agent ---


def create_researcher_agent_node():
    """
    Creates the researcher agent node.
    This agent uses Tavily to search for information and summarizes it.
    """
    research_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a highly skilled research assistant. Your goal is to gather comprehensive and relevant information from the web based on the user's question.
         Use the provided Tavily search tool (by explicitly outputting 'CALL_TOOL: [search query]') to find information.
         After searching, summarize your findings.
         If you believe enough information has been gathered to answer the question, state 'RESEARCH_COMPLETE'.
         If more research is needed, state 'RESEARCH_NEEDED' followed by what specific information you are looking for, or another 'CALL_TOOL: [search query]' to refine your search.
         
         Current research context: {research_results}
         Current question: {question}
         """),
        ("human",
         "{question}\n\nBased on the current context, what should be the next step (e.g., 'CALL_TOOL: [query]', 'RESEARCH_COMPLETE', or 'RESEARCH_NEEDED [explanation]')?")
    ])

    research_chain = (
        {"question": RunnablePassthrough(), "research_results": RunnablePassthrough()}
        | research_prompt
        | llm
        | StrOutputParser()
    )

    def run_researcher(state: AgentState):
        """
        Runs the researcher agent to gather information and decide next steps.
        """
        print(
            f"\n--- RESEARCHER AGENT (Iteration {state['iterations'] + 1}) ---")

        research_context = "\n".join(
            state["research_results"]) if state["research_results"] else "No prior research conducted."

        # Invoke the LLM to get its decision/summary
        decision_output = research_chain.invoke(
            {"question": state["question"], "research_results": research_context})

        # Check if the LLM decided to call a tool (search)
        if decision_output.startswith("CALL_TOOL:"):
            search_query = decision_output.replace("CALL_TOOL:", "").strip()
            print(f"Researcher decided to search for: '{search_query}'")
            try:
                # Store the raw results from Tavily to debug
                raw_search_results = tavily_tool.invoke(search_query)
                print(
                    f"DEBUG: Raw search results type: {type(raw_search_results)}")
                print(
                    f"DEBUG: Raw search results content (first 200 chars): {str(raw_search_results)[:200]}")

                new_research = []
                # TavilySearch typically returns a list of dictionaries.
                # Each dict has 'url' and 'content' keys.
                if isinstance(raw_search_results, list):
                    for res in raw_search_results:
                        if isinstance(res, dict) and 'url' in res and 'content' in res:
                            new_research.append(
                                f"Source: {res['url']}\nContent: {res['content']}")
                        else:
                            # If an element in the list is not a dictionary or lacks keys
                            print(
                                f"WARNING: Unexpected format for a search result item: {res}")
                            new_research.append(
                                f"Problematic search result item: {res}")
                elif isinstance(raw_search_results, str):
                    # This means Tavily returned an error string directly
                    print(
                        f"ERROR: Tavily returned a string, likely an API error: {raw_search_results}")
                    new_research.append(
                        f"Tavily API Error: {raw_search_results}")
                else:
                    # Catch any other unexpected types
                    print(
                        f"WARNING: Unhandled search result type from Tavily: {type(raw_search_results)}")
                    new_research.append(
                        f"Unhandled Tavily result: {raw_search_results}")

                if not new_research and raw_search_results:
                    # If raw results exist but couldn't be parsed into structured research
                    new_research.append(
                        f"No structured research found, raw response: {raw_search_results}")

                print(f"Found {len(new_research)} new research snippets.")
                return {
                    "research_results": state["research_results"] + new_research,
                    "iterations": state["iterations"] + 1,
                }
            except Exception as e:
                # This catches exceptions from the tavily_tool.invoke itself or subsequent processing
                print(f"Error during search or processing results: {e}")
                return {
                    "research_results": state["research_results"] + [f"Error searching for '{search_query}': {e}"],
                    "iterations": state["iterations"] + 1,
                }
        elif "RESEARCH_COMPLETE" in decision_output:
            print("Researcher declared research complete.")
            return {
                "research_results": state["research_results"] + [f"Researcher concluded: {decision_output}"],
                "iterations": state["iterations"] + 1,
            }
        else:  # RESEARCH_NEEDED or just a summary without explicit action
            print("Researcher suggests more steps or provided a summary.")
            return {
                "research_results": state["research_results"] + [f"Researcher's thoughts: {decision_output}"],
                "iterations": state["iterations"] + 1,
            }

    return run_researcher


# --- Answer Drafter Agent ---
def create_drafter_agent_node():
    """
    Creates the answer drafter agent node.
    This agent takes research findings and drafts a comprehensive answer.
    """
    drafter_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert answer drafter. Your task is to synthesize the provided research results into a clear, comprehensive, and well-structured answer to the user's question.
         Ensure all relevant points from the research are covered. If the research is insufficient, state that more information is needed.
         
         Original question: {question}
         
         Research results:
         {research_results}
         
         Draft your answer below, starting with "Final Answer:".
         """),
        ("human", "{question}")
    ])

    drafter_chain = (
        {"question": RunnablePassthrough(), "research_results": RunnablePassthrough()}
        | drafter_prompt
        | llm
        | StrOutputParser()
    )

    def run_drafter(state: AgentState):
        """
        Runs the drafting agent to synthesize an answer.
        """
        print("\n--- DRAFTER AGENT ---")
        research_context = "\n".join(
            state["research_results"]) if state["research_results"] else "No research provided."

        response = drafter_chain.invoke(
            {"question": state["question"], "research_results": research_context})

        print("Drafter has produced an answer.")
        return {"drafted_answer": response}

    return run_drafter


# Instantiate the agent nodes
researcher_node = create_researcher_agent_node()
drafter_node = create_drafter_agent_node()
