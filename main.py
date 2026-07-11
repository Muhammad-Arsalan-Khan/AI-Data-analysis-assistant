import streamlit as st
import pandas as pd
import os
from analysis import clean_and_load, ask_gemini
import matplotlib.pyplot as plt
from io import BytesIO

# --- REAL PDF GENERATOR ---
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(question, answer):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    
    # Custom Styling for PDF
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#1E88E5'),
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#FFB300'),
        spaceBefore=15,
        spaceAfter=10
    )
    
    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['BodyText'],
        fontSize=11,
        leading=16,
        spaceAfter=10
    )
    
    # Document Content
    story.append(Paragraph("📊 AI Data Analytics - Executive Summary", title_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("🔍 User Query / Question Asked:", heading_style))
    story.append(Paragraph(question, body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("🤖 Gemini AI Detailed Insights:", heading_style))
    # Replacing newlines with break tags for PDF formatting
    formatted_answer = answer.replace('\n', '<br/>')
    story.append(Paragraph(formatted_answer, body_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# --- STREAMLIT UI CONFIGURATION ---
st.set_page_config(
    page_title="AI Data Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-title { font-size: 38px; font-weight: bold; color: #1E88E5; text-align: center; margin-bottom: 20px; }
    .stButton>button { width: 100%; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 Advanced AI Data Analytics Dashboard</div>', unsafe_allow_html=True)

# SIDEBAR
st.sidebar.header("⚙️ Control Panel")
uploaded_file = st.sidebar.file_uploader("Upload your Dataset (CSV format)", type=["csv"])
chart_type = st.sidebar.selectbox("Select Visualization Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart"])

if uploaded_file is not None:
    try:
        with open("temp_dataset.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        df = clean_and_load("temp_dataset.csv")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📋 Dataset Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            st.subheader("🤖 Ask Gemini AI about Data")
            user_question = st.text_input("Enter your query regarding the dataset:")
            
            if st.button("Analyze with AI"):
                if user_question:
                    with st.spinner("Gemini is thinking..."):
                        try:
                            answer = ask_gemini(df, user_question)
                            st.success("🤖 AI Analysis:")
                            st.write(answer)
                            
                            # --- STORES RECENT ANALYSIS IN SESSION STATE FOR DOWNLOAD ---
                            st.session_state['recent_q'] = user_question
                            st.session_state['recent_a'] = answer
                            
                        except Exception as ai_err:
                            st.error(f"AI Error: {ai_err}")
                else:
                    st.warning("Please type a question first!")
            
            # Show PDF download button if analysis is ready
            if 'recent_q' in st.session_state:
                pdf_data = generate_pdf_report(st.session_state['recent_q'], st.session_state['recent_a'])
                st.download_button(
                    label="📥 Export Analysis as PDF",
                    data=pdf_data,
                    file_name="AI_Data_Analysis_Report.pdf",
                    mime="application/pdf"
                )

        with col2:
            st.subheader("📈 Dynamic Visualization")
            try:
                fig, ax = plt.subplots(figsize=(6, 4))
                numeric_cols = df.select_dtypes(include=['number']).columns
                object_cols = df.select_dtypes(include=['object', 'category']).columns
                
                if len(df) > 0:
                    if chart_type == "Bar Chart" and len(object_cols) > 0:
                        df[object_cols[0]].value_counts().head(10).plot(kind='bar', ax=ax, color='#1E88E5')
                    elif chart_type == "Line Chart" and len(numeric_cols) > 0:
                        df[numeric_cols[0]].head(50).plot(kind='line', ax=ax, color='#FFB300')
                    elif chart_type == "Scatter Plot" and len(numeric_cols) > 1:
                        ax.scatter(df[numeric_cols[0]].head(50), df[numeric_cols[1]].head(50), color='#4CAF50')
                    elif chart_type == "Pie Chart" and len(object_cols) > 0:
                        df[object_cols[0]].value_counts().head(5).plot(kind='pie', ax=ax, autopct='%1.1f%%')
                    else:
                        df.iloc[:, 0].value_counts().head(5).plot(kind='bar', ax=ax)
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # EXPORT CHART
                    buf = BytesIO()
                    fig.savefig(buf, format="png", bbox_inches='tight')
                    st.download_button(
                        label="🖼️ Export Chart as PNG",
                        data=buf.getvalue(),
                        file_name=f"{chart_type.lower().replace(' ', '_')}.png",
                        mime="image/png"
                    )
            except Exception as vis_err:
                st.error(f"Visualization Error: {vis_err}")

    except Exception as general_err:
        st.error(f"File Error: {general_err}")
else:
    st.info("👋 Welcome! Please upload a CSV file from the sidebar to start.")