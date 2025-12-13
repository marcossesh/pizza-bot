import os
from typing import Annotated, Literal, TypedDict

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from app.tools import get_pizza_price, add_to_order, get_menu
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

tools = [get_pizza_price, add_to_order, get_menu]
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = """Você é o Pizza Bot, um assistente virtual de uma pizzaria.
Seu objetivo é ajudar os clientes a ver o cardápio, consultar preços e fazer pedidos.

REGRAS CRÍTICAS:
1. Quando a ferramenta `get_menu` for chamada, o retorno dela conterá a lista de pizzas.
2. VOCÊ É OBRIGADO A COPIAR E COLAR ESSA LISTA NA SUA RESPOSTA FINAL.
3. NÃO RESUMA. NÃO DIGA APENAS "AQUI ESTÁ". MOSTRE A LISTA.
4. Se a ferramenta retornar "Cardápio: ...", sua resposta DEVE conter "Cardápio: ...".

Responda sempre em português do Brasil de forma educada e prestativa."""

def chatbot(state: AgentState):
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    return {"messages": [llm_with_tools.invoke(messages)]}

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
