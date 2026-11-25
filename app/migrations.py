from app.core.database import Base, engine

# Import models so they register on Base.metadata before create_all runs.
from app.modules.user import models  # noqa: F401

def run_migrations():
    Base.metadata.create_all(bind=engine)