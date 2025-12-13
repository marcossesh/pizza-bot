from sqlmodel import select
from app.models import Pizza
from app.database import get_session
import logging

logger = logging.getLogger("pizzabot")

async def seed_pizzas():
    # Create a generator to get the session
    session_generator = get_session()
    session = await session_generator.__anext__()
    
    try:
        result = await session.exec(select(Pizza))
        pizzas = result.all()
        
        if not pizzas:
            initial_pizzas = [
                Pizza(name="Calabresa", ingredients="Molho de tomate, queijo, calabresa e cebola", price=40.00),
                Pizza(name="Mussarela", ingredients="Molho de tomate, queijo mussarela e orégano", price=35.00),
                Pizza(name="Portuguesa", ingredients="Molho de tomate, queijo, presunto, ovo, cebola e azeitona", price=45.00),
            ]
            
            for pizza in initial_pizzas:
                session.add(pizza)
            
            await session.commit()
            logger.info("Database seeded successfully!")
        else:
            logger.info("Database already seeded.")
            
    finally:
        await session.close()
