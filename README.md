# 🤖 Autonomous AI Agent Framework

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Cyclic_Workflows-orange)
![Gemini](https://img.shields.io/badge/Model-Gemini_2.5_Flash-purple)
![Docker](https://img.shields.io/badge/Deployment-Docker_Container-blue)

A production-ready **Autonomous AI Agent** built with **LangGraph** and **FastAPI**. Unlike traditional linear chains, this agent utilizes a **cyclic state graph**, allowing it to "reason, act, and observe" iteratively. It can autonomously browse the web (via Tavily) to fetch real-time data and generate reports without human intervention.

## 🏗️ Architecture

The system uses a **Cognitive Architecture** where the LLM (Gemini) acts as the brain, maintaining state across multiple turns of execution.

```mermaid
graph TD
    User[User / API Request] -->|POST /run-agent| API[FastAPI Endpoint]
    API -->|Initialize State| Agent[Agent Node (Gemini 2.5)]
    
    Agent -->|Decision| Router{Tools Needed?}
    
    Router -->|Yes| Tools[Tool Node]
    Router -->|No| End[Final Response]
    
    Tools -->|Web Search (Tavily)| Internet((Internet))
    Tools -->|Save Report| FileSys[(File System)]
    
    Tools -->|Update State| Agent
    
    subgraph "Cyclic Execution Loop"
    Agent
    Router
    Tools
    end
```

## 🚀 Key Features

- **Cyclic Reasoning Loop**: Uses LangGraph to enable multi-step workflows (e.g., "Search -> Read -> Search Again -> Answer").
- **Real-Time Knowledge**: Integrated with Tavily AI Search to bypass the LLM's knowledge cutoff (access to 2025 data).
- **Production API**: Wrapped in FastAPI for easy integration with frontends or microservices.
- **Containerized**: Fully Dockerized environment using Docker-in-Docker for consistent deployment on GitHub Codespaces or AWS.

## 🛠️ Tech Stack

- **LLM**: Google Gemini 2.5 Flash (via langchain-google-genai)
- **Orchestration**: LangChain & LangGraph (Stateful Graphs)
- **Tools**: Tavily Search API, File System
- **Backend**: FastAPI, Uvicorn
- **DevOps**: Docker, GitHub Codespaces

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.11+ or Docker
- API Keys: `GOOGLE_API_KEY`, `TAVILY_API_KEY`

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-agent-framework.git
cd ai-agent-framework
```

### 2. Environment Setup

Create a `.env` file in the root or export variables directly:

```bash
export GOOGLE_API_KEY="your_gemini_key"
export TAVILY_API_KEY="your_tavily_key"
```

### 3. Run with Docker (Recommended)

Build and run the container to ensure environment consistency.

```bash
docker build -t ai-agent .
docker run -p 8000:8000 --env-file .env ai-agent
```

### 4. Local Development

```bash
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔌 Usage

Send a POST request to the agent. It will autonomously decide if it needs to search the web.

### Example Request:

```bash
curl -X POST "http://localhost:8000/run-agent" \
     -H "Content-Type: application/json" \
     -d '{"query": "What are the key MLOps trends in late 2025?"}'
```

### Example Response:

```json
{
  "status": "success",
  "response": "Based on the latest search results from Dec 2025, the key trends are..."
}
```

## 📂 Project Structure

```
├── src/
│   ├── agent.py      # Core LangGraph logic (Nodes, Edges, State)
│   ├── tools.py      # Tool definitions (Tavily Search, Report Saver)
│   ├── main.py       # FastAPI entry point
│   └── __init__.py
├── Dockerfile        # Container configuration
├── requirements.txt  # Pinned dependencies for stability
└── README.md         # Documentation
```

## 🎯 What Next? (Portfolio Strategy)

You now have a fully functional project. To make this "stick" in your portfolio:

1. **Commit everything:**
   ```bash
   git add .
   git commit -m "feat: complete agent framework with Tavily and Gemini 2.5"
   git push
   ```

2. **Screenshot the Success:** Take a screenshot of your VS Code terminal showing the successful `curl` response about 2025 trends.

3. **LinkedIn Post:** You can now post specifically about "Solving the Knowledge Cutoff problem using Agentic Workflows with LangGraph."