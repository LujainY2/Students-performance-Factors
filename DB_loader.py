import pandas as pd
from sqlalchemy import create_engine ,text

from urllib.parse import quote_plus

from Studentpipeline import run_pipeline

# =========================================
# 1. Create the Database
# =========================================

def create_db(db_name):
    """Create a PostgreSQL database if it doesn't exist."""

    password = quote_plus("10203040")

    admin_engine = create_engine(
        f"postgresql://postgres:{password}@localhost:5432/postgres",
        isolation_level="AUTOCOMMIT"
    )

    try:
        with admin_engine.connect() as conn:

            # Check if database exists
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
                {"db_name": db_name}
            )

            if result.fetchone() is None:

                # Create database
                # Validate the identifier before inserting it into SQL
                if not db_name.isidentifier():
                    raise ValueError("Invalid database name")

                conn.execute(
                    text(f'CREATE DATABASE "{db_name}"')
                )

                print(f"Database created: {db_name}")

            else:
                print(f"Database already exists: {db_name}")

    finally:
        # Close engine connections
        admin_engine.dispose()

# =========================================
# 2. Connect to the Database
# =========================================
    """ connect to the target Postgresql DB. """
def conn_to_db(db_name):
    
    password = quote_plus("10203040")
    
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

import pandas as pd
from sqlalchemy import text

def verify_load(engine, table_name):
    """Run verification queries against the loaded table."""

    with engine.connect() as conn:

        # =========================================
        # 4.1 Row Count
        # =========================================

        result = conn.execute(
            text(f'SELECT COUNT(*) FROM "{table_name}"')
        )

        row_count = result.scalar()
        print(f"Rows count: {row_count}")

        # =========================================
        # 4.2 Column Count
        # =========================================

        result = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM information_schema.columns
                WHERE table_name = :table_name
                  AND table_schema = current_schema()
            """),
            {"table_name": table_name}
        )

        col_count = result.scalar()
        print(f"Columns count: {col_count}")

        # =========================================
        # 4.3 Data Preview
        # =========================================

        df_check = pd.read_sql(
            text(f'SELECT * FROM "{table_name}" LIMIT 5'),
            conn
        )

        print("\nData Preview:")
        print(df_check.to_string(index=False))

        # =========================================
        # 4.4 NULL Checks
        # =========================================

        result = conn.execute(
            text(
                f'SELECT COUNT(*) FROM "{table_name}" '
                'WHERE "Exam_Score" IS NULL'
            )
        )

        total_nulls = result.scalar()

        print(f"\nNULLs in Exam_Score: {total_nulls}")

        # =========================================
        # 4.5 Verification Status
        # =========================================

        if row_count > 0 and col_count > 0:
            print("\nVerification Passed")
        else:
            print("\nVerification Failed")


# =========================================
# 5. Run the Load
# =========================================
def run_loader(filepath,db_name,table_name):
    """ Full ETL: clean CSV file >> Load in postgres SQL"""
    print("="*50)
    print("DB Loader Starts")
    print("="*50)
    
    # using the same function we created while cleaning
    df = run_pipeline(filepath)
    
    print("\n ---- Database Loading ----")
    
    create_db(db_name)
    
    engine = conn_to_db(db_name)
    
    load_to_database(df,engine,table_name)
    
    verify_load(engine,table_name)
    
    # stop connection 
    engine.dispose()
    
    print("\n"+"-"*50)
    
    print("DB Loader Complete")
    
    print("-"*50)
    

if __name__=="__main__":
        run_loader(
            filepath="StudentPerformanceFactors.csv",
            db_name='student_analytics_db',
            table_name='students'
        )