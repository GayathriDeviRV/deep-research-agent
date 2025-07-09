from graph import build_graph
from state import AgentState


def run_deep_research_agent(question: str):
    """
    Runs the deep research agentic system for a given question.
    """
    app = build_graph()

    initial_state: AgentState = {
        "question": question,
        "research_results": [],
        "drafted_answer": "",
        "iterations": 0
    }

    print(f"Starting Deep Research for: '{question}'")

    # Initialize a current_state that will accumulate updates
    current_state = initial_state.copy()  # Start with a copy of the initial state

    # Iterate through the stream to see intermediate steps and accumulate state
    for s in app.stream(initial_state):
        print(s)  # Print the update yielded by the current node
        # Each 's' is a dictionary where keys are node names and values are the state updates from that node.
        # We need to merge these updates into our current_state.
        for node_name, node_output in s.items():
            current_state.update(node_output)

    print("\n--- FINAL ANSWER ---")
    # Now, current_state should hold the full, accumulated state after all nodes have run.
    if current_state and "drafted_answer" in current_state and current_state["drafted_answer"]:
        print(current_state["drafted_answer"])
    else:
        print("No final answer drafted or an error occurred during drafting.")
        print("\n--- Final State Snapshot ---")
        # Print relevant parts of the final state for debugging if no answer
        print(f"Question: {current_state.get('question', 'N/A')}")
        print(f"Iterations: {current_state.get('iterations', 'N/A')}")
        print("Research Results:")
        for i, res in enumerate(current_state.get('research_results', [])):
            # Print first 100 chars of each result
            print(f"  [{i+1}] {res[:100]}...")
        print(
            f"Drafted Answer (raw): {current_state.get('drafted_answer', 'N/A')}")


if __name__ == "__main__":
    user_question = input("Enter your research question: ")
    run_deep_research_agent(user_question)
