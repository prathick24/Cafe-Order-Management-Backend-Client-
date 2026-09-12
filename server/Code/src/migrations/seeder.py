# migrations/seeder.py
from sqlalchemy.orm import Session
from repositories.database import Database
from repositories.schemas.schema import Item


class Seeder:
    def __init__(self):
        self.db = Database()
        
    def seed_data(self):
        session = self.db.SessionLocal()
        try:
            # Seed skills
            if not session.query(Item).first():
                items = [
                   Item(item_name="Espresso" , item_price = 300.00),
                   Item(item_name="Cappuccino" , item_price = 350.00 ),
                   Item(item_name="Latte" , item_price = 350.00),
                   Item(item_name="Americano" , item_price = 250.00 ),
                   Item(item_name="Mocha" , item_price = 300.00),
                   Item(item_name="Hot Chocolate" , item_price = 290.00),
                   Item(item_name="Masala Chai" , item_price = 140.00),
                   Item(item_name="Cold Brew" , item_price = 240.00),
                   Item(item_name="Flat White" , item_price = 200.00)
                   ]
                session.add_all(items)
                session.flush()
                
            
           
            session.commit()
            print("✓ Database seeded successfully")
            
        except Exception as e:
            session.rollback()
            print(f"✗ Error seeding database: {str(e)}")
            raise e
        finally:
            session.close()

    def run_startup_seeding(self):
        """Run seeding on FastAPI startup"""
        self.seed_data()

if __name__ == "__main__":
    seeder = Seeder()
    seeder.seed_data()