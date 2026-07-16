import pandas as pd
import numpy as np
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

def clean_and_load(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip().str.lower()
    return df

# 🌟 DYNAMIC FIXED: 'selected_cols' parameter yahan add kar diya hai
def ask_gemini(df, question, custom_key=None, num_rows=10, selected_cols=None):
    api_key = custom_key if custom_key else os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("API Key missing")

    client = genai.Client(api_key=api_key)
    
    # Agar user ne columns select kiye hain toh sirf wahi bhejo, warna saare
    cols_to_use = selected_cols if selected_cols else list(df.columns)
    
    # Filter rows and columns dynamically
    sampled_df = df[cols_to_use].head(num_rows)
    
    data_summary = f"""
    Dataset Total Dimensions: {len(df)} rows x {len(df.columns)} columns
    Analyzed Columns: {', '.join(cols_to_use)}
    Analyzed Rows for Context: {num_rows}
    Sample Data Filtered:\n{sampled_df.to_string()}
    """
    
    prompt = f"Based on this filtered data summary:\n{data_summary}\n\nAnswer this question: {question}"
    
    response = client.models.generate_content(
        model="gemini-3.5-flash", 
        contents=prompt,
    )
    return response.text