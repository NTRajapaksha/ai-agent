from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from src.agent import agent_app

app = FastAPI(title="AI Agent API")

class TaskRequest(BaseModel):
    query: str

@app.post("/run-agent")
def run_agent(request: TaskRequest):
    """
    Endpoint to trigger the AI Agent.
    """
    initial_state = {"messages": [HumanMessage(content=request.query)]}
    
    # Run the graph until completion
    result = agent_app.invoke(initial_state)
    
    # Extract the last message content (the final answer)
    final_response = result["messages"][-1].content
    return {"status": "success", "response": final_response}