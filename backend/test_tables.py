from app.db.database import engine
from app.models.models import Base
from sqlalchemy import inspect

# Create all tables
Base.metadata.create_all(bind=engine)

# Check what tables exist
inspector = inspect(engine)
tables = inspector.get_table_names()

print("Tables in database:")
for table in tables:
    print(f"  - {table}")

# Check specifically for summary tables
summary_tables = [t for t in tables if t.startswith('summary_')]
print(f"\nFound {len(summary_tables)} summary tables")