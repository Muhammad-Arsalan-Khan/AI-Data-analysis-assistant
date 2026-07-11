# import pandas as pd
# import numpy as np
# import os
# from google import genai
# from dotenv import load_dotenv  

# # .env file se automatic fresh key uthane ke liye
# load_dotenv()

# def clean_and_load(file_path):
#     df = pd.read_csv(file_path)
#     df.columns = df.columns.str.strip().str.lower()
#     return df

# def ask_gemini(df, question):
#     # Kisi os.environ ki zaroorat nahi hai yahan!
#     # genai.Client() background mein khud hi .env se fresh key dhoond lega.
#     client = genai.Client()
    
#     # Data Summary for Context
#     data_summary = f"""
#     Dataset Columns: {', '.join(df.columns)}
#     Total Records: {len(df)}
#     Sample Data:\n{df.head(3).to_string()}
#     """
    
#     prompt = f"Based on this data summary:\n{data_summary}\n\nAnswer this question: {question}"
    
#     response = client.models.generate_content(
#         model="gemini-3.5-flash",
#         contents=prompt,
#     )
#     return response.text





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

def ask_gemini(df, question, custom_key=None, num_rows=10):
    # 🌟 LOCAL VS LIVE HYBRID LOGIC
    # Agar custom key di hai toh wo use karo, nahi toh system (.env) ki key check karo
    api_key = custom_key if custom_key else os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("API Key missing")

    client = genai.Client(api_key=api_key)
    
    # 🌟 USER DEFINED ROWS FOR AI CONTEXT
    # Pure dataset ke bajaye user ki demand ke mutabiq slice karte hain
    sampled_df = df.head(num_rows)
    
    data_summary = f"""
    Dataset Columns: {', '.join(df.columns)}
    Total Rows in Dataset: {len(df)}
    Analyzed Rows for Context: {num_rows}
    Sample Data:\n{sampled_df.to_string()}
    """
    
    prompt = f"Based on this data summary:\n{data_summary}\n\nAnswer this question: {question}"
    
    response = client.models.generate_content(
        model="gemini-3.5-flash", 
        contents=prompt,
    )
    return response.text