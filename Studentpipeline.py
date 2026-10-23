
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
    df.select_dtypes(include=["object", "category"]).columns)
    
    print(f"Numeric columns: {numeric_col}")
    print(f"Categorical columns: {categorical_col}")
    
    return df


# =========================================
# 4. Handeling Missing Values
# =========================================

def handle_missing(df):
    df =df.copy()
    
    #  fill missing values in categorical columns 
    for col in df.select_dtypes(include=["object", "category"]).columns:
        if df[col].isnull().sum() > 0:
            mode_values = df[col].mode()

            if not mode_values.empty:
                fill_value = mode_values.iloc[0]

                df[col] = df[col].fillna(fill_value)

                print(f"Filled {col} with mode: {fill_value}")
            
    #  fill missing values in numeric columns 
    for col in df.select_dtypes(include=["number"]).columns:
        if df[col].isnull().sum()>0:
            fill_value = df[col].meadian()
            
            df[col] = df[col].fillna(fill_value)
            
            print(f'filled {col} with median:{fill_value}')

    # check missing values 
    remaining_nulls = df.isnull().sum().sum()
    print(f'Remaining nulls:{remaining_nulls}')
    return df

# =========================================
# 5. Standarize text
# ========================================= 

def Standarize_text(df):
    df = df.copy()

    categorical_cols = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for col in categorical_cols:
        df[col] = df[col].str.strip().str.title()

    print(f"Standardized {len(categorical_cols)} categorical columns")

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
# =========================================   
def add_features(df):
    df = df.copy()
    # ordener : there is relation bet values ex low,m,l
    # nominal : no relation like female
    # Encode 
    df['Motivation_Level'] = df['Motivation_Level'].map(
        {
            "Low":1,
            "Medium":2,
            "High":3
        }
    ) 

    df['Has_Internet'] = df['Internet_Access'].map(
            {
                "Yes":1,
                "No":0,
            }
        ) 
    df['Pass_Fail'] = np.where(
        df['Exam_Score']>=65,
        "Pass" ,"Fail"
    )
    # Create Score Bands 
    df["Score_Band"] = pd.cut(
    df["Exam_Score"],
    bins=[0, 60, 70, 80, 90, 101],
    labels=["Very Low", "Low", "Medium", "High", "Very High"]
)
    
    new_col = ['Motivation_Level','Has_internet','Pass_Fail',"Score_Band"]
    
    print(f'Added {len(new_col)} Features :{new_col}')
    
    return df
# =========================================
# 8. Summary
# =========================================  

def general_summary(df):
    print("\n === Analytics Summary ===")
    print(f"Total Students:{len(df)} Students")
    
    avg_score = df["Exam_Score"].mean()
    print(f"Avg Exam Score : {avg_score:.1f} %")
    
    
    pass_rate = (df["Pass_Fail"]=="Pass").mean()*100
    print(f"Pass Rate {pass_rate:.1f} %")
    # Statistics by Motivation 
    
    print("\n Score by Motivation Level:")
    
    mot_sts = df.groupby(
        "Motivation_Level",
        observed = True).agg(
            avg_score = ("Exam_Score","mean"),
            count = ("Exam_Score","count")
            
        ).round(1)
        
    print(mot_sts.to_string(index = True))
    
    return df
    
def run_pipeline(filepath): 
    print("="*50)
    print("Cleaning pipeline")
    print("="*50)

    print("Ingest Data")
    df = ingest_data(filepath)
    
    print("Inspect Data")
    print()
    df = inspect_data(df)
    
    print("\n --- Cleaning ---- ")
    
    print("Standarization")
    df = Standarize_text(df)
    
    print("Removing duplicates")
    df = Remove_duplicates(df)
    
    print("Handeling Missing Values")
    df = handle_missing(df)
    
    print("\n ---- Enrichment ----")
    df = add_features(df)
    
    print("Analytics Summary")
    df = general_summary(df)
    
    print("\n"+ "="*50)
    print(
        f"Pipeline Completed {df.shape[0]} rows,{df.shape[1]} columns"
    )
    print("\n"+ "="*50)
    return df 


if __name__=="__main__":
    clean_data= run_pipeline("StudentPerformanceFactors.csv")
    
    clean_data.to_csv("Cleaned_StudentPerformance.csv")
    print("cleaned data Saved Successfully!")



