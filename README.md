# deep-research-agent
This project implements a sophisticated deep research agent powered by Large Language Models (LLMs) and a web search tool. It leverages LangGraph for orchestration, allowing autonomous agents to collaborate on a research task, and LangChain for interacting with LLMs and tools. The system can iteratively search for information and then synthesize it into a comprehensive answer.

---

## Features

- **Iterative Research**: Conducts multiple rounds of web searches to gather rich context.
- **Modular Agents**: Separates responsibilities into distinct agents:
  - **Researcher**: Gathers and processes information.
  - **Drafter**: Synthesizes a final answer.
- **LLM Integration**: Uses Hugging Face models (specifically `meta-llama/Llama-3.1-405B-Instruct`) via `langchain-huggingface`.
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

## Setup and Installation

### Clone the Repository

```bash
git clone https://github.com/GayathriDeviRV/deep-research-agent
cd deep-research-agent
```

### Create a Virtual Environment

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

### Configure Environment Variables

Create a .env file in the root directory and add:

```bash
TAVILY_API_KEY="your_tavily_api_key"
HF_TOKEN="your_huggingface_token"
```
- Get your Tavily API key from [Tavily](https://www.tavily.com/)
- Get your Hugging Face token from your [Hugging Face settings](https://huggingface.co/settings/tokens) with access to meta-llama/Llama-3.1-405B-Instruct.

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## How to Run

Run the research agent using:

```bash
python main.py
```

You'll be prompted with:

```bash
Enter your research question:
```
Type in your query and hit Enter. The agent will:
- Perform web searches
- Pass information between agents
- Output a comprehensive final draft

---

## Example Usage

Enter your research question: tell about the silent patient book

Starting Deep Research for: 'tell about the silent patient book'

... (intermediate research and drafting steps will be printed here) ...

--- FINAL ANSWER ---
Final Answer:

The Silent Patient is a psychological thriller novel by Alex Michaelides that tells the story of Alicia Berenson, a painter who murders her husband of seven years, Gabriel Berenson, and refuses to speak or explain her actions. The novel follows the story of Theo Faber, a psychotherapist who becomes obsessed with uncovering the truth behind Alicia's silence.

The book has received positive reviews for its intelligent character study and masterful plotting. Reviewers have praised the novel's unique approach to the psychological thriller genre, with one reviewer stating that it "forges its own path" in the genre. The book has also been described as a "shocking" and "thought-provoking" read.

The primary narrator of the novel is Theo Faber, a psychotherapist who becomes obsessed with Alicia's case. However, some reviewers have noted that Theo is a faulty character, and that the book portrays him as being good at his job despite his own flaws.

The novel explores themes of trauma, mental illness, and the complexities of human relationships. The author's use of language and plotting has been praised for its ability to keep readers engaged and guessing until the very end.

Overall, The Silent Patient is a gripping and thought-provoking novel that has received widespread critical acclaim for its unique approach to the psychological thriller genre. If you're a fan of psychological thrillers or are looking for a book that will keep you on the edge of your seat, The Silent Patient is definitely worth checking out.
