import os
from typing import Annotated, Literal, TypedDict

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from app.tools import get_pizza_price, add_to_order
import logging

logger = logging.getLogger("pizzabot")

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    order_items: list[str]
    total_cost: float


# Ensure GROQ_API_KEY is set in environment variables
if not os.environ.get("GROQ_API_KEY"):
    logger.warning("GROQ_API_KEY not found in environment variables.")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

tools = [get_pizza_price, add_to_order]
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: AgentState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder = StateGraph(AgentState)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools))

graph_builder.set_entry_point("chatbot")

def tools_condition(state: AgentState) -> Literal["tools", "__end__"]:
    messages = state["messages"]
    last_message = messages[-1]
    
    if last_message.tool_calls:
        return "tools"
    return "__end__"

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

graph_builder.add_edge("tools", "chatbot")

graph = graph_builder.compile()
