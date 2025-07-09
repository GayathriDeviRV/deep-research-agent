from typing import TypedDict, List


class AgentState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: The initial question to research.
        research_results: A list of strings containing raw research findings.
        drafted_answer: The answer drafted by the drafting agent.
        iterations: How many research iterations have occurred.
    """
    question: str
    research_results: List[str]
    drafted_answer: str
    iterations: int
