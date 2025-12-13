import os
from typing import Annotated, Literal, TypedDict

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

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

REGRAS CRÍTICAS DE FERRAMENTAS:
1. `get_menu`: Use APENAS quando o usuário pedir explicitamente para ver o cardápio ou opções.
2. `add_to_order`: Use quando o usuário quiser fazer um pedido (ex: "quero uma", "adicione", "vou levar").
   - Se o usuário não disser o nome da pizza (ex: "quero uma"), USE O CONTEXTO da conversa para identificar qual pizza ele está falando (a última mencionada).
   - Se não houver pizza no contexto, pergunte qual pizza ele deseja.

REGRAS DE EXIBIÇÃO:
1. Quando a ferramenta `get_menu` for chamada, VOCÊ É OBRIGADO A COPIAR E COLAR A LISTA RETORNADA NA SUA RESPOSTA.
2. NÃO RESUMA O CARDÁPIO. Mostre todos os itens retornados pela ferramenta.

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

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)
