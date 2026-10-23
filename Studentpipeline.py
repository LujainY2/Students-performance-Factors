
# =========================================
# 1. Importing the Libraries
# =========================================

import pandas as pd
import numpy as np


# =========================================
# 2. Data Ingestion
# =========================================

def ingest_data(file_path):
    df = pd.read_csv(file_path)

    print(f"Loaded: {file_path}")
    print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")

    return df


# =========================================
# 3. Data Inspection
# =========================================

def inspect_data(df):

    # Check missing values
    nulls = df.isnull().sum()
    null_columns = nulls[nulls > 0]

    if not null_columns.empty:
        print("\nColumns with missing values:")

        for col, count in null_columns.items():
            percentage = (count / len(df)) * 100
            print(f"{col}: {count} ({percentage:.1f}%)")
    else:
        print("\nNo missing values found.")

    # Check duplicates
    duplicates = df.duplicated().sum()
    print(f"\nDuplicate rows: {duplicates}")

    # Check data types
    numeric_col = len(
        df.select_dtypes(include="number").columns
    )

    categorical_col = len(
        df.select_dtypes(include=["object", "category", "string"]).columns
    )

    print(f"Numeric columns: {numeric_col}")
    print(f"Categorical columns: {categorical_col}")
    
    return df


# =========================================
# 4. Handeling Missing Values
# =========================================

def handle_missing(df):
    df =df.copy()
    
    #  fill missing values in categorical columns 
    for col in df.select_dtypes(include=["object","str"]).columns:
        if df[col].isnull().sum()>0:
            fill_value = df[col].mode()[0]
            
            df[col] = df[col].fillna(fill_value)
            
            print(f'filled {col} with mode:{fill_value}')
            
    #  fill missing values in numeric columns 
    for col in df.select_dtypes(include=["number"]).columns:
        if df[col].isnull().sum()>0:
            fill_value = df[col].meadian()
            
            df[col] = df[col].fillna(fill_value)
            
            print(f'filled {col} with median:{fill_value}')

# check missing values 
remaining_nulls = df.isnull().sum().sum()
print(f'Remaining nulls:{remaining_nulls}')

# =========================================
# 5. Standarize text
# ========================================= 

def Standarize_text(df):
    df = df.copy()
    categorical_col = df.select_dtypes(include=['object','str']).columns
    
    for col in categorical_col:
        df[col]= df[col].strip().str.title()
        
    print(f"Standarized {len(categorical_col)} categorical columns")
    
    return df

# =========================================
# 6. Remove Duplicates
# =========================================     
    
def Remove_duplicates(df):
    df = df.copy()
    before = len(df)
    df = df.drop_duplicates()
    removed= before- len(df)
    print(f"Removed {removed} duplicated rows")
    
    return df

# =========================================
# 7. Feature Engineering
# =========================================   s


 

df = ingest_data("StudentPerformanceFactors.csv")

# Display the first five rows
print(df.head())

# Inspect the dataset
inspect_data(df)
