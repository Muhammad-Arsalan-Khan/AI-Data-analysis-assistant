import pandas as pd
import numpy as np
import os
from google import genai
from dotenv import load_dotenv  

# .env file se automatic fresh key uthane ke liye
load_dotenv()

def clean_and_load(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip().str.lower()
    return df

def ask_gemini(df, question):
    # Kisi os.environ ki zaroorat nahi hai yahan!
    # genai.Client() background mein khud hi .env se fresh key dhoond lega.
    client = genai.Client()
    
    # Data Summary for Context
    data_summary = f"""
    Dataset Columns: {', '.join(df.columns)}
    Total Records: {len(df)}
    Sample Data:\n{df.head(3).to_string()}
    """
    
    prompt = f"Based on this data summary:\n{data_summary}\n\nAnswer this question: {question}"
    
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )
    return response.text