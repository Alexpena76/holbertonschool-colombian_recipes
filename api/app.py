"""
Colombian Recipe API - Entry Point
"""
from app import create_app, db
from app.models import *

# Create the Flask application
app = create_app()


@app.cli.command('seed')
def seed_database():
    """Seed the database with initial data"""
    from app.models.category import Category
    from app.models.recipe import Recipe
    from app.models.ingredient import Ingredient
    from app.models.step import Step
    
    print("Seeding database...")
    
    # Check if already seeded
    if Category.query.count() > 0:
        print("Database already seeded!")
        return
    
    # Categories
    categories = [
        Category('breakfast', 'Breakfast', 'Desayuno'),
        Category('lunch', 'Lunch', 'Almuerzo'),
        Category('dinner', 'Dinner', 'Cena'),
        Category('dessert', 'Dessert', 'Postre'),
        Category('snack', 'Snack', 'Antojo'),
        Category('drinks', 'Drinks', 'Bebidas'),
    ]
    db.session.add_all(categories)
    db.session.commit()
    print(f"Added {len(categories)} categories")
    
    print("Database seeded successfully!")


@app.cli.command('create-tables')
def create_tables():
    """Create all database tables"""
    db.create_all()
    print("Tables created successfully!")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
