import pandas as pd
from sqlalchemy import create_engine ,text

from urllib.parse import quote_plus

from Studentpipeline import run_pipeline

# =========================================
# 1. Create the Database
# =========================================

def crete_db(db_name):
    """ to create a PostgresSQL database if it doesnt exist. """
    password = quote_plus('lKlK12@@') 
    
    # obj
    admin_engine = create_engine(
        f'postgresql://postgres:{password}@localhost:5432/postgres',
        isolation_level ="AUTOCOMMIT"
    )
    
    with admin_engine.connect() as conn:
        #check if db name exist 
        result= conn.excute(text(f"SELECT 1 FROM pd_database WHERE datname= '{db_name}'"))
        if result.fetchone() is None:
            # db not exist >> create db
            conn.excute(
            text(f"CREATE DATABASE {db_name}")
            )
        else:
            print(f"DB is Exists:{db_name}")
        
    # close connection 
    admin_engine.dispose()

# =========================================
# 2. Connect to the Database
# =========================================
    """ connect to the target Postgresql DB. """
def conn_to_db(db_name):
    
    password = quote_plus("lKlK12@@")
    
    engine = create_engine(
            f'postgresql://postgres:{password}@localhost:5432/{db_name}',
        )
    
    print(f'Connected to :{db_name}')
    
    return engine

# =========================================
# 3. Load Data into Database
# =========================================
    
def load_to_database(df,engine,table_name):
    """Load the DataFrame into Postgresql table"""
    
    df.to_sql(
        name  = table_name,
        con = engine, 
        if_exists ='replace',
        index=False
    )
    
    print(f"Loaded {len(df)} rows into table: {table_name}")

# =========================================
# 4. Verify Load
# =========================================


def verify_load(engine,table_name):
    """ Run verification Queries against theloaded table"""
    with engine.connect as conn:
        # rows count
        result= conn.execute(
            text(f'SELECT COUNT(*) FROM {table_name}')
            
        )
        
        row_count = result.scalar()
        
        print(f'Rows count: {row_count}')
        
        result = conn.execute(
            text(f'SELECT COUNT(*) FROM information_schema.columns'
                f'WHERE table_name = {table_name}' )
        )
        col_count = result.scalar()
        print(f'Columns count: {col_count}')
        
        df_check = pd.read_sql(
            f'SELECT * FROM {table_name} LIMIT 5',
            engine
        )
        
        print("\n Preview (print head):")
        print(df_check.to_string(index=False))
        
        #Null checks 
        
        df_nulls = pd.read_sql(
            f'SELECT COUNT(*) as total_nulls from {table_name}'
            f'where "Exam_Score" is null',
            engine
        )

        print(f'\n Nulls in Exam_scores:{df_nulls['total_nulls'].iloc[0]}')
        
        print('\n Verification Passed')
