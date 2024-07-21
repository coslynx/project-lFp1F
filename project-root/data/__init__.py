from .models import Database

# Initialize the database connection
database = Database()

# Create tables or collections if they don't exist
database.create_tables()