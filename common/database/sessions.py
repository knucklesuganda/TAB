from sqlalchemy.orm import sessionmaker
from common.database.database_setup import engine

Session = sessionmaker(bind=engine)
