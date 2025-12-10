import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from typing import Annotated, TypedDict
import operator
from langchain_core.messages import SystemMessage
from datetime import datetime

# Import our custom tools
from src.tools import web_search, save_report

# 1. Setup API Key (loaded automatically from Codespace secrets)
if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# 2. Define the State (The Agent's Memory)
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]

# 3. Initialize Gemini Model & Bind Tools
# We use gemini-1.5-flash for speed/cost or gemini-1.5-pro for complex reasoning
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0)
tools = [web_search, save_report]
llm_with_tools = llm.bind_tools(tools)

# 4. Define Nodes
def agent_node(state: AgentState):
    """The node where the LLM decides what to do."""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 5. Build the Graph
workflow = StateGraph(AgentState)

def agent_node(state: AgentState):
    messages = state["messages"]
    
    # Create a System Message with the current date
    # This tricks the LLM into knowing it is "now"
    current_date = datetime.now().strftime("%B %Y")
    system_prompt = SystemMessage(
        content=f"You are a helpful AI assistant. Today is {current_date}. "
                f"You have access to a web search tool. "
                f"If the user asks for current trends, news, or information from {current_date}, "
                f"YOU MUST use the 'web_search' tool to find the answer. "
                f"Do not refuse to answer. Search first."
    )
    
    # Prepend the system prompt to the conversation
    # We use a trick: [system_prompt] + messages
    # But for the graph state, we just invoke the model with the hint
    response = llm_with_tools.invoke([system_prompt] + messages)
    
    return {"messages": [response]}

# Add nodes
workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(tools))

# Add edges
workflow.set_entry_point("agent")

# conditional_edges checks: Does the LLM want to call a tool? 
# If yes -> go to "tools". If no (it's finished) -> END.
workflow.add_conditional_edges(
    "agent",
    tools_condition, 
)

workflow.add_edge("tools", "agent") # Loop back to agent after tool usage

# Compile the graph
agent_app = workflow.compile()