def main(db_path):
    import os
    from sqlalchemy import create_engine
    from models import Base

    # Create a SQLite database if it doesn't exist
    if not os.path.exists(db_path):
        engine = create_engine(db_path)

        # Create all tables in the database
        Base.metadata.create_all(engine)


