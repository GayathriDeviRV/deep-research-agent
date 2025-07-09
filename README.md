# deep-research-agent
An autonomous AI system that leverages LangGraph and web search to iteratively research and synthesize comprehensive answers to user questions.

---

## Features

- **Iterative Research**: Conducts multiple rounds of web searches to gather rich context.
- **Modular Agents**: Separates responsibilities into distinct agents:
  - **Researcher**: Gathers and processes information.
  - **Drafter**: Synthesizes a final answer.
- **LLM Integration**: Uses Hugging Face models (default: `meta-llama/Llama-3.1-405B-Instruct`) via `langchain-huggingface`.
- **Web Search**: Integrates with **Tavily Search API** for real-time information retrieval.
- **Configurable**: Easily switch LLMs and API keys.

---

## Project Structure

| File/Folder       | Purpose |
|-------------------|---------|
| `.env`            | Stores API keys securely. |
| `requirements.txt`| Lists required Python dependencies. |
| `state.py`        | Defines the shared `AgentState` object to pass data between agents. |
| `llm_tools.py`    | Initializes the LLM and Tavily search tool. |
| `agents.py`       | Contains the logic for `researcher_node` and `drafter_node`. |
| `graph.py`        | Builds the LangGraph workflow and defines transitions between agents. |
| `main.py`         | Entry point: runs the agentic system and displays output. |

---
