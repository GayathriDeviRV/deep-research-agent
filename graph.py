from langgraph.graph import StateGraph, END
from typing import Literal
from state import AgentState
from agents import researcher_node, drafter_node


def should_continue_research(state: AgentState) -> Literal["research", "draft"]:
    """
    Decides whether to continue researching or proceed to drafting.
    This decision is based on a heuristic (e.g., iterations, or checking agent output).
    """
    print(f"\n--- DECIDER: Current Iterations: {state['iterations']} ---")

    if state["iterations"] < 3 and "RESEARCH_COMPLETE" not in "".join(state["research_results"][-1:]):
        print("Continuing research...")
        return "research"
    else:
        print("Proceeding to drafting.")
        return "draft"


def build_graph():
    workflow = StateGraph(AgentState)

    # Add nodes for each agent
    workflow.add_node("research", researcher_node)
    workflow.add_node("draft", drafter_node)

    # Set the entry point
    workflow.set_entry_point("research")

    # Define edges (transitions)
    # Researcher -> Decision Point
    workflow.add_conditional_edges(
        "research",
        should_continue_research,
        {
            "research": "research",  # If more research is needed, loop back to researcher
            "draft": "draft",        # If research is complete, go to drafter
        }
    )

    # Drafter -> END
    workflow.add_edge("draft", END)

    # Compile the graph
    app = workflow.compile()
    return app


if __name__ == "__main__":
    # Test the graph (optional, for debugging the graph structure)
    graph_app = build_graph()
    print("Graph built successfully.")
