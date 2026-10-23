import pandas as pd
from sqlalchemy import create_engine ,text

from urllib.parse import quote_plus

from Studentpipeline import run_pipeline

# =========================================
# Create the Database
# =========================================

def crete_db(db_name):
    """ to create a PostgresSQL database if it doesnt exist. """
    password = quote_plus('lKlK12@@') 
    
    # obj
    admin_engine = create_engine(
        f'postgresql://postgres:{password}@localhost:5432/postgres',
        isolation_level ="AUTOCOMMIT"
    )












