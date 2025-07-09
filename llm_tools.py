import os
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# --- LLM Setup ---
LLM_MODEL = "meta-llama/Llama-3.1-405B-Instruct"


def get_llm():
    """Initializes and returns the HuggingFaceEndpoint LLM wrapped for chat."""
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise ValueError("HF_TOKEN environment variable not set.")

    # First, initialize the HuggingFaceEndpoint (the underlying connection)
    # Ensure this is correctly configured for your specific Hugging Face Inference API setup.
    # If you are specifically using Fireworks.ai, this is where it might be implicitly routed.
    base_llm = HuggingFaceEndpoint(
        repo_id=LLM_MODEL,
        huggingfacehub_api_token=hf_token,
        temperature=0.7,
        max_new_tokens=2048,
        top_k=50,
        top_p=0.95,
    )

    # Now, wrap it with ChatHuggingFace to use the conversational task
    llm = ChatHuggingFace(llm=base_llm)
    return llm

# --- Tools Setup ---


def get_tavily_tool():
    """Initializes and returns the Tavily search tool."""
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        raise ValueError("TAVILY_API_KEY environment variable not set.")

    # Use the new TavilySearch class
    tool = TavilySearch(max_results=5)  # Adjust max_results as needed
    return tool


# Export LLM and tool instances
llm = get_llm()
tavily_tool = get_tavily_tool()

if __name__ == "__main__":
    print("LLM and Tavily tool initialized successfully.")
    # Quick test for chat model
    from langchain_core.messages import HumanMessage, SystemMessage
    try:
        messages = [
            SystemMessage(content="You are a helpful AI assistant."),
            HumanMessage(content="What is the capital of France?")
        ]
        response = llm.invoke(messages)
        print(f"Chat LLM Test: {response.content[:50]}...")
    except Exception as e:
        print(f"Chat LLM Test failed: {e}")

    try:
        search_result = tavily_tool.invoke("latest AI advancements")
        print(f"Tavily Test: {search_result[0]['content'][:50]}...")
    except Exception as e:
        print(f"Tavily Test failed: {e}")
