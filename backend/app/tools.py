from langchain_core.tools import tool
from sqlmodel import select
from app.database import get_session
from app.models import Pizza
import logging

logger = logging.getLogger("pizzabot")

@tool
async def get_pizza_price(pizza_name: str) -> str:
    """
    Consulta o preço e os ingredientes de uma pizza no banco de dados.
    Use esta ferramenta quando o usuário perguntar o preço de uma pizza ou o que vem nela.
    """

    logger.info(f"Searching for pizza: {pizza_name}")
    
    session_generator = get_session()
    session = await session_generator.__anext__()
    
    try:
        statement = select(Pizza).where(Pizza.name.ilike(f"%{pizza_name}%"))
        result = await session.exec(statement)
        pizza = result.first()
        
        if pizza:
            logger.info(f"Found pizza: {pizza.name}")
            return f"A pizza de {pizza.name} custa R$ {pizza.price:.2f} e leva {pizza.ingredients}."
        else:
            logger.warning(f"Pizza not found: {pizza_name}")
            return f"Desculpe, não encontrei a pizza de {pizza_name} no cardápio."
            
    except Exception as e:
        logger.error(f"Error querying database: {str(e)}", exc_info=True)
        return f"Erro ao consultar o banco de dados: {str(e)}"
        
    finally:
        await session.close()

@tool
async def add_to_order(pizza_name: str, quantity: int = 1) -> str:
    """Use esta ferramenta quando o usuário confirmar que quer pedir uma pizza."""
    logger.info(f"Adding to order: {quantity}x {pizza_name}")
    
    session_generator = get_session()
    session = await session_generator.__anext__()
    
    try:
        statement = select(Pizza).where(Pizza.name.ilike(f"%{pizza_name}%"))
        result = await session.exec(statement)
        pizza = result.first()
        
        if pizza:
            total = pizza.price * quantity
            logger.info(f"Added {quantity}x {pizza.name} to order. Total: {total}")
            return f"Adicionado {quantity}x {pizza.name} ao pedido. Valor unitário: R$ {pizza.price:.2f}. Subtotal: R$ {total:.2f}"
        else:
            logger.warning(f"Pizza not found for order: {pizza_name}")
            return f"Desculpe, não encontrei a pizza de {pizza_name} para adicionar ao pedido."
            
    except Exception as e:
        logger.error(f"Error adding to order: {str(e)}", exc_info=True)
        return f"Erro ao processar pedido: {str(e)}"
        
    finally:
        await session.close()
