# import streamlit as st
# import pandas as pd
# import os
# from analysis import clean_and_load, ask_gemini
# import matplotlib.pyplot as plt
# from io import BytesIO
# from dotenv import load_dotenv

# load_dotenv()

# # Real PDF Generator Setup
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib import colors

# def generate_pdf_report(question, answer):
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
#     story = []
#     styles = getSampleStyleSheet()
#     title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor('#1E88E5'), spaceAfter=20)
#     heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#FFB300'), spaceBefore=15, spaceAfter=10)
#     body_style = ParagraphStyle('Body', parent=styles['BodyText'], fontSize=11, leading=16, spaceAfter=10)
#     story.append(Paragraph("📊 AI Data Analytics - Executive Summary", title_style))
#     story.append(Spacer(1, 10))
#     story.append(Paragraph("🔍 User Query:", heading_style))
#     story.append(Paragraph(question, body_style))
#     story.append(Spacer(1, 10))
#     story.append(Paragraph("🤖 Gemini AI Insights:", heading_style))
#     story.append(Paragraph(answer.replace('\n', '<br/>'), body_style))
#     doc.build(story)
#     buffer.seek(0)
#     return buffer

# # --- DYNAMIC THEME ENGINE ---
# if 'theme' not in st.session_state:
#     st.session_state['theme'] = 'dark'

# st.sidebar.header("🎨 Theme Customization")
# theme_choice = st.sidebar.radio("Select App Mode:", ["🌙 Dark Mode", "☀️ Light Mode"], 
#                                 index=0 if st.session_state['theme'] == 'dark' else 1)

# if "Dark" in theme_choice:
#     st.session_state['theme'] = 'dark'
#     bg_color = "#121212"
#     text_color = "#FFFFFF"
#     card_bg = "#1E1E1E"
#     plot_theme = 'dark_background'
# else:
#     st.session_state['theme'] = 'light'
#     bg_color = "#F8F9FA"
#     text_color = "#000000"
#     card_bg = "#FFFFFF"
#     plot_theme = 'default'

# st.markdown(f"""
#     <style>
#     .stApp {{ background-color: {bg_color}; color: {text_color}; }}
#     .main-title {{ font-size: 38px; font-weight: bold; color: #1E88E5; text-align: center; margin-bottom: 20px; }}
#     .stButton>button {{ width: 100%; border-radius: 8px; }}
#     </style>
#     """, unsafe_allow_html=True)

# st.markdown('<div class="main-title">📊 Advanced AI Data Analytics Dashboard</div>', unsafe_allow_html=True)

# # SIDEBAR CONTROLS
# st.sidebar.markdown("---")
# st.sidebar.header("⚙️ Control Panel")

# env_key_exists = os.getenv("GEMINI_API_KEY") is not None
# user_api_key = None
# if not env_key_exists:
#     user_api_key = st.sidebar.text_input("🔑 Enter Your Gemini API Key", type="password")
#     if not user_api_key:
#         st.sidebar.warning("⚠️ Live Mode Active: Provide API key to unlock AI Analytics.")
# else:
#     st.sidebar.success("✅ Local Mode: Secure System API Key Loaded.")

# uploaded_file = st.sidebar.file_uploader("Upload your Dataset (CSV format)", type=["csv"])

# if uploaded_file is not None:
#     try:
#         with open("temp_dataset.csv", "wb") as f:
#             f.write(uploaded_file.getbuffer())
        
#         df = clean_and_load("temp_dataset.csv")
#         all_columns = list(df.columns)
        
#         col1, col2 = st.columns([1, 1])
        
#         with col1:
#             st.subheader("📋 Dataset Preview")
#             st.dataframe(df, height=250, use_container_width=True)
            
#             # 🌟 1. NEW FEATURE: AUTOMATED DATA METRICS SUMMARY ENGINE
#             st.subheader("📉 Automated Structural & Statistical Summary")
            
#             # Row & Column Dimension Metrics Cards
#             c_rows, c_cols = st.columns(2)
#             c_rows.metric("Total Rows", f"{len(df):,}")
#             c_cols.metric("Total Columns", len(df.columns))
            
#             # Structural Base Table (Column Name, Data Type, Null Values)
#             summary_data = []
#             for col in df.columns:
#                 summary_data.append({
#                     "Column Name": col,
#                     "Data Type": str(df[col].dtype),
#                     "Null Values": int(df[col].isnull().sum())
#                 })
#             summary_df = pd.DataFrame(summary_data)
            
#             st.markdown("**🔬 Column Meta Matrix (Types & Nulls):**")
#             st.dataframe(summary_df, height=200, use_container_width=True)
            
#             # Statistical Segment Split
#             numeric_cols = df.select_dtypes(include=['number']).columns
#             categorical_cols = df.select_dtypes(include=['object', 'category']).columns
            
#             # Numerical Statistics Table (Mean, Max, Min, Count)
#             if len(numeric_cols) > 0:
#                 st.markdown("**🔢 Numerical Profile (Count, Mean, Min, Max):**")
#                 num_desc = df[numeric_cols].describe().loc[['count', 'mean', 'min', 'max']].T
#                 st.dataframe(num_desc, height=200, use_container_width=True)
                
#             # Categorical Analytics Table (Value Counts & Percentages)
#             if len(categorical_cols) > 0:
#                 st.markdown("**🔤 Categorical Value Distribution:**")
#                 cat_choice = st.selectbox("Select Category Column to View Distribution:", categorical_cols)
                
#                 counts = df[cat_choice].value_counts().head(20)
#                 percentages = df[cat_choice].value_counts(normalize=True).head(20) * 100
                
#                 cat_distribution_df = pd.DataFrame({
#                     "Value Count": counts,
#                     "Percentage (%)": percentages.round(2).astype(str) + '%'
#                 })
#                 st.dataframe(cat_distribution_df, height=200, use_container_width=True)

#             # AI Section
#             st.subheader("🤖 Ask Gemini AI about Data")
#             max_rows = len(df)
#             rows_to_analyze = st.slider("🔢 Select rows to send to AI for Context:", min_value=5, max_value=min(max_rows, 500), value=min(max_rows, 20))
#             user_question = st.text_input("Enter your query regarding the dataset:")
            
#             has_access = env_key_exists or (user_api_key and user_api_key.strip() != "")
            
#             if has_access:
#                 if st.button("Analyze with AI"):
#                     if user_question:
#                         with st.spinner("Gemini is thinking..."):
#                             try:
#                                 answer = ask_gemini(df, user_question, custom_key=user_api_key, num_rows=rows_to_analyze)
#                                 st.success("🤖 AI Analysis:")
#                                 st.write(answer)
#                                 st.session_state['recent_q'] = user_question
#                                 st.session_state['recent_a'] = answer
#                             except Exception as ai_err:
#                                 st.error(f"AI Error: API operational failure. Details: {ai_err}")
#                     else:
#                         st.warning("Please type a question first!")
#             else:
#                 st.error("🔒 AI Feature Locked: Enter a valid Gemini API key in the sidebar.")

#             if 'recent_q' in st.session_state:
#                 pdf_data = generate_pdf_report(st.session_state['recent_q'], st.session_state['recent_a'])
#                 st.download_button(label="📥 Export Analysis as PDF", data=pdf_data, file_name="AI_Data_Analysis_Report.pdf", mime="application/pdf")

#         with col2:
#             st.subheader("📈 Custom Visualization Engine")
#             chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram"])
            
#             needs_y_axis = chart_type not in ["Pie Chart", "Histogram"]
#             x_column = st.selectbox("Select X-Axis Column", all_columns)
            
#             if needs_y_axis:
#                 y_column = st.selectbox("Select Y-Axis Column", all_columns, key="y_enabled")
#             else:
#                 st.selectbox("Select Y-Axis Column (Not needed for this chart)", ["None / Disabled"], disabled=True, key="y_disabled")
#                 y_column = None

#             custom_title = st.text_input("Chart Title", value=f"{chart_type} of {x_column}")
#             custom_xlabel = st.text_input("X-Axis Label", value=x_column)
            
#             if needs_y_axis:
#                 custom_ylabel = st.text_input("Y-Axis Label", value=y_column)
#             else:
#                 custom_ylabel = st.text_input("Y-Axis Label", value="Frequency / Value", disabled=True)
                
#             chart_color = st.color_picker("Pick Chart Theme Color", "#1E88E5")

#             try:
#                 plt.style.use(plot_theme)
#                 fig, ax = plt.subplots(figsize=(6, 4))
                
#                 if chart_type == "Bar Chart":
#                     df.groupby(x_column)[y_column].mean().head(15).plot(kind='bar', ax=ax, color=chart_color)
#                 elif chart_type == "Line Chart":
#                     df.head(50).plot(kind='line', x=x_column, y=y_column, ax=ax, color=chart_color)
#                 elif chart_type == "Scatter Plot":
#                     ax.scatter(df[x_column].head(100), df[y_column].head(100), color=chart_color, alpha=0.7)
#                 elif chart_type == "Pie Chart":
#                     df[x_column].value_counts().head(5).plot(kind='pie', ax=ax, autopct='%1.1f%%')
#                 elif chart_type == "Histogram":
#                     df[x_column].plot(kind='hist', ax=ax, bins=15, color=chart_color, edgecolor=text_color, alpha=0.8)
                
#                 ax.set_title(custom_title, color=text_color)
#                 ax.set_xlabel(custom_xlabel, color=text_color)
#                 ax.set_ylabel(custom_ylabel, color=text_color)
                
#                 fig.patch.set_facecolor(bg_color)
#                 ax.set_facecolor(card_bg)
                
#                 plt.tight_layout()
#                 st.pyplot(fig)
                
#                 buf = BytesIO()
#                 fig.savefig(buf, format="png", bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
#                 st.download_button(label="🖼️ Export Custom Chart as PNG", data=buf.getvalue(), file_name=f"custom_{chart_type.lower()}.png", mime="image/png")
                
#             except Exception as vis_err:
#                 st.error(f"Visualization Logic Mismatch: {vis_err}")

#     except Exception as general_err:
#         st.error(f"File Parsing Error: {general_err}")
# else:
#     st.info("👋 Welcome! Please configure settings from the sidebar and upload a data template.")






# import streamlit as st
# import pandas as pd
# import os
# from analysis import clean_and_load, ask_gemini
# import matplotlib.pyplot as plt
# from io import BytesIO
# from dotenv import load_dotenv

# load_dotenv()

# # Real PDF Generator Setup
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib import colors

# def generate_pdf_report(question, answer):
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
#     story = []
#     styles = getSampleStyleSheet()
#     title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor('#1E88E5'), spaceAfter=20)
#     heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#FFB300'), spaceBefore=15, spaceAfter=10)
#     body_style = ParagraphStyle('Body', parent=styles['BodyText'], fontSize=11, leading=16, spaceAfter=10)
#     story.append(Paragraph("AI Data Analytics - Executive Summary", title_style))
#     story.append(Spacer(1, 10))
#     story.append(Paragraph("User Query:", heading_style))
#     story.append(Paragraph(question, body_style))
#     story.append(Spacer(1, 10))
#     story.append(Paragraph("Gemini AI Insights:", heading_style))
#     story.append(Paragraph(answer.replace('\n', '<br/>'), body_style))
#     doc.build(story)
#     buffer.seek(0)
#     return buffer

# # --- DYNAMIC THEME ENGINE ---
# if 'theme' not in st.session_state:
#     st.session_state['theme'] = 'dark'

# st.sidebar.header("Theme Customization")
# theme_choice = st.sidebar.radio("Select App Mode:", ["Dark Mode", "Light Mode"], 
#                                 index=0 if st.session_state['theme'] == 'dark' else 1)

# if "Dark" in theme_choice:
#     st.session_state['theme'] = 'dark'
#     bg_color = "#121212"
#     text_color = "#FFFFFF"
#     card_bg = "#1E1E1E"
#     plot_theme = 'dark_background'
# else:
#     st.session_state['theme'] = 'light'
#     bg_color = "#F8F9FA"
#     text_color = "#000000"
#     card_bg = "#FFFFFF"
#     plot_theme = 'default'

# # 🌟 PREMIUM RESPONSIVE NAVBAR INTERACTIVE CSS (FIXED SIDEBAR OVERLAP)
# st.markdown(f"""
#     <style>
#     /* Global Smooth Scroll Trigger */
#     html, body, [data-testid="stAppViewContainer"] {{
#         scroll-behavior: smooth !important;
#         background-color: {bg_color};
#         color: {text_color};
#     }}
    
#     /* Content Layer Layout Push */
#     [data-testid="stMainBlockContainer"] {{
#         padding-top: 130px !important;
#     }}
    
#     .main-title {{ font-size: 38px; font-weight: bold; color: #1E88E5; text-align: center; margin-bottom: 10px; }}
    
#     /* 🌟 FIX: RESPONSIVE FLEXBOX NAVBAR CONTEXT (Chote Buttons Aur Left Sidebar Padding Offset) */
#     .fixed-header-navbar {{
#         position: fixed;
#         top: 55px; 
#         left: 0;
#         width: 100%;
#         background-color: {bg_color};
#         z-index: 99999;
#         padding: 25px 5% 12px 22%; /* Increased left padding (22%) to completely push buttons away from sidebar */
#         border-bottom: 2px solid #1E88E5;
#         box-shadow: 0px 6px 12px rgba(0,0,0,0.2);
#         box-sizing: border-box;
#     }}
    
#     /* Responsive Flex Containers instead of Rigid Grid */
#     .nav-button-container {{
#         display: flex;
#         justify-content: space-between;
#         align-items: center;
#         gap: 12px;
#         width: 100%;
#         max-width: 900px; /* Locks max width so buttons don't blow up */
#     }}
    
#     /* Premium Compact Button Styling */
#     .nav-btn {{
#         flex: 1;
#         text-align: center;
#         box-sizing: border-box;
#         padding: 8px 4px; /* Reduced vertical & horizontal padding for smaller uniform sizes */
#         background-color: #1E88E5;
#         color: white !important;
#         text-decoration: none !important;
#         border-radius: 6px;
#         font-weight: 600;
#         font-size: 13px; /* Smaller font matrix */
#         letter-spacing: 0.3px;
#         white-space: nowrap; /* Forces text to stay in single line */
#         transition: all 0.2s ease-in-out;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.15);
#     }}
#     .nav-btn:hover {{
#         background-color: #1565C0;
#         transform: translateY(-2px);
#         box-shadow: 0 4px 10px rgba(30, 136, 229, 0.3);
#     }}
#     .nav-btn:active {{
#         transform: translateY(0);
#         background-color: #0D47A1;
#     }}
    
#     /* Anchor Scroll Target Tuning Offset */
#     div[id^="section-"] {{
#         scroll-margin-top: 160px; 
#     }}
    
#     /* Streamlit Global Actions Buttons Overrides (Export & Analyze) */
#     div.stButton > button {{
#         width: 100% !important;
#         background-color: #1E88E5 !important;
#         color: white !important;
#         border: none !important;
#         padding: 10px 10px !important;
#         border-radius: 6px !important;
#         font-weight: bold !important;
#         font-size: 14px !important;
#         transition: all 0.25s ease-in-out !important;
#     }}
#     div.stButton > button:hover {{
#         background-color: #1565C0 !important;
#     }}

#     /* SCROLL REVEAL VIEW ANIMATION STYLES */
#     .reveal-slide-up {{
#         animation: revealSlideUp 0.8s cubic-bezier(0.25, 1, 0.5, 1) both;
#     }}
#     .reveal-zoom-in {{
#         animation: revealZoomIn 0.8s cubic-bezier(0.25, 1, 0.5, 1) both;
#     }}
    
#     @keyframes revealSlideUp {{
#         0% {{ opacity: 0; transform: translateY(30px); }}
#         100% {{ opacity: 1; transform: translateY(0); }}
#     }}
#     @keyframes revealZoomIn {{
#         0% {{ opacity: 0; transform: scale(0.97) translateY(15px); }}
#         100% {{ opacity: 1; transform: scale(1) translateY(0); }}
#     }}
#     </style>
#     """, unsafe_allow_html=True)

# st.markdown('<div class="main-title">Advanced AI Data Analytics Dashboard</div>', unsafe_allow_html=True)

# # SIDEBAR CONTROLS
# st.sidebar.markdown("---")
# st.sidebar.header("Control Panel")

# env_key_exists = os.getenv("GEMINI_API_KEY") is not None
# user_api_key = None
# if not env_key_exists:
#     user_api_key = st.sidebar.text_input("Enter Your Gemini API Key", type="password")
#     if not user_api_key:
#         st.sidebar.warning("Live Mode Active: Provide API key to unlock AI Analytics.")
# else:
#     st.sidebar.success("Local Mode: Secure System API Key Loaded.")

# uploaded_file = st.sidebar.file_uploader("Upload your Dataset (CSV format)", type=["csv"])

# if uploaded_file is not None:
#     try:
#         with open("temp_dataset.csv", "wb") as f:
#             f.write(uploaded_file.getbuffer())
        
#         df = clean_and_load("temp_dataset.csv")
#         all_columns = list(df.columns)
        
#         # 🌟 FIXED COMPACT NAVBAR HEADER WITH RIGHT SIDEBAR SHIFT
#         st.markdown(f"""
#             <div class="fixed-header-navbar">
#                 <div class="nav-button-container">
#                     <a href="#section-preview" class="nav-btn">Preview Data</a>
#                     <a href="#section-summary" class="nav-btn">Data Summary</a>
#                     <a href="#section-viz" class="nav-btn">Visualization</a>
#                     <a href="#section-ai" class="nav-btn">Analyze With AI</a>
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)
        
#         # 🌟 SECTION 1: PREVIEW DATA
#         st.markdown('<div id="section-preview" class="reveal-slide-up">', unsafe_allow_html=True)
#         st.subheader("Dataset Preview")
#         st.dataframe(df, height=250, use_container_width=True)
#         st.markdown('</div>', unsafe_allow_html=True)
#         st.markdown("<br/><br/>", unsafe_allow_html=True)
        
#         # 🌟 SECTION 2: DATA SUMMARY
#         st.markdown('<div id="section-summary" class="reveal-zoom-in">', unsafe_allow_html=True)
#         st.subheader("Automated Structural & Statistical Summary")
        
#         c_rows, c_cols = st.columns(2)
#         c_rows.metric("Total Rows", f"{len(df):,}")
#         c_cols.metric("Total Columns", len(df.columns))
        
#         summary_data = []
#         for col in df.columns:
#             summary_data.append({
#                 "Column Name": col,
#                 "Data Type": str(df[col].dtype),
#                 "Null Values": int(df[col].isnull().sum())
#             })
#         summary_df = pd.DataFrame(summary_data)
#         st.markdown("**Column Meta Matrix (Types & Nulls):**")
#         st.dataframe(summary_df, height=200, use_container_width=True)
        
#         numeric_cols = df.select_dtypes(include=['number']).columns
#         categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        
#         if len(numeric_cols) > 0:
#             st.markdown("**Numerical Profile:**")
#             num_desc = df[numeric_cols].describe().loc[['count', 'mean', 'min', 'max']].T
#             st.dataframe(num_desc, height=200, use_container_width=True)
            
#         if len(categorical_cols) > 0:
#             st.markdown("**Categorical Value Distribution:**")
#             cat_choice = st.selectbox("Select Category Column to View Distribution:", categorical_cols)
#             counts = df[cat_choice].value_counts().head(20)
#             percentages = df[cat_choice].value_counts(normalize=True).head(20) * 100
#             cat_distribution_df = pd.DataFrame({"Value Count": counts, "Percentage (%)": percentages.round(2).astype(str) + '%'})
#             st.dataframe(cat_distribution_df, height=200, use_container_width=True)
#         st.markdown('</div>', unsafe_allow_html=True)
#         st.markdown("<br/><br/>", unsafe_allow_html=True)

#         # 🌟 SECTION 3: CUSTOM VISUALIZATION ENGINE
#         st.markdown('<div id="section-viz" class="reveal-slide-up">', unsafe_allow_html=True)
#         st.subheader("Custom Visualization Engine")
        
#         v_col1, v_col2 = st.columns([1, 1])
#         with v_col1:
#             chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram"])
#             needs_y_axis = chart_type not in ["Pie Chart", "Histogram"]
#             x_column = st.selectbox("Select X-Axis Column", all_columns)
            
#             if needs_y_axis:
#                 y_column = st.selectbox("Select Y-Axis Column", all_columns, key="y_enabled")
#             else:
#                 st.selectbox("Select Y-Axis Column (Not needed)", ["None / Disabled"], disabled=True, key="y_disabled")
#                 y_column = None
                
#             custom_title = st.text_input("Chart Title", value=f"{chart_type} of {x_column}")
#             custom_xlabel = st.text_input("X-Axis Label", value=x_column)
#             custom_ylabel = st.text_input("Y-Axis Label", value=y_column if needs_y_axis else "Frequency / Value", disabled=not needs_y_axis)
#             chart_color = st.color_picker("Pick Chart Theme Color", "#1E88E5")

#         with v_col2:
#             try:
#                 plt.style.use(plot_theme)
#                 fig, ax = plt.subplots(figsize=(6, 4))
                
#                 if chart_type == "Bar Chart":
#                     df.groupby(x_column)[y_column].mean().head(15).plot(kind='bar', ax=ax, color=chart_color)
#                 elif chart_type == "Line Chart":
#                     df.head(50).plot(kind='line', x=x_column, y=y_column, ax=ax, color=chart_color)
#                 elif chart_type == "Scatter Plot":
#                     ax.scatter(df[x_column].head(100), df[y_column].head(100), color=chart_color, alpha=0.7)
#                 elif chart_type == "Pie Chart":
#                     df[x_column].value_counts().head(5).plot(kind='pie', ax=ax, autopct='%1.1f%%')
#                 elif chart_type == "Histogram":
#                     df[x_column].plot(kind='hist', ax=ax, bins=15, color=chart_color, edgecolor=text_color, alpha=0.8)
                
#                 ax.set_title(custom_title, color=text_color)
#                 ax.set_xlabel(custom_xlabel, color=text_color)
#                 ax.set_ylabel(custom_ylabel, color=text_color)
#                 fig.patch.set_facecolor(bg_color)
#                 ax.set_facecolor(card_bg)
#                 plt.tight_layout()
#                 st.pyplot(fig)
                
#                 buf = BytesIO()
#                 fig.savefig(buf, format="png", bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
#                 st.download_button(label="Export Custom Chart as PNG", data=buf.getvalue(), file_name=f"custom_{chart_type.lower()}.png", mime="image/png")
#             except Exception as vis_err:
#                 st.error(f"Visualization Mismatch Error: {vis_err}")
#         st.markdown('</div>', unsafe_allow_html=True)
#         st.markdown("<br/><br/>", unsafe_allow_html=True)

#         # 🌟 SECTION 4: ASK GEMINI AI ABOUT DATA
#         st.markdown('<div id="section-ai" class="reveal-zoom-in">', unsafe_allow_html=True)
#         st.subheader("Ask Gemini AI about Data")
        
#         ai_col1, ai_col2 = st.columns([1, 1])
#         with ai_col1:
#             selected_ai_columns = st.multiselect(
#                 "Select specific Columns to send to AI Context:",
#                 options=all_columns,
#                 default=all_columns[:3] if len(all_columns) > 3 else all_columns
#             )
            
#             max_rows = len(df)
#             rows_to_analyze = st.slider("Select rows to send to AI for Context:", min_value=5, max_value=min(max_rows, 500), value=min(max_rows, 20))
#             user_question = st.text_input("Enter your query regarding the dataset:")
            
#             has_access = env_key_exists or (user_api_key and user_api_key.strip() != "")
            
#             if has_access:
#                 if st.button("Analyze with AI"):
#                     if user_question:
#                         with st.spinner("Gemini is thinking..."):
#                             try:
#                                 answer = ask_gemini(df, user_question, custom_key=user_api_key, num_rows=rows_to_analyze, selected_cols=selected_ai_columns)
#                                 st.session_state['recent_q'] = user_question
#                                 st.session_state['recent_a'] = answer
#                             except Exception as ai_err:
#                                 st.error(f"AI Error: API operational failure. Details: {ai_err}")
#                     else:
#                         st.warning("Please type a question first!")
#             else:
#                 st.error("AI Feature Locked: Enter a valid Gemini API key in the sidebar.")

#         with ai_col2:
#             if 'recent_a' in st.session_state:
#                 st.success("AI Analysis Insights:")
#                 st.write(st.session_state['recent_a'])
                
#                 pdf_data = generate_pdf_report(st.session_state['recent_q'], st.session_state['recent_a'])
#                 st.download_button(label="Export Analysis as PDF", data=pdf_data, file_name="AI_Data_Analysis_Report.pdf", mime="application/pdf")
#         st.markdown('</div>', unsafe_allow_html=True)

#     except Exception as general_err:
#         st.error(f"File Parsing Error: {general_err}")
# else:
#     st.info("Welcome! Please configure settings from the sidebar and upload a data template.")




import streamlit as st
import pandas as pd
import os
from analysis import clean_and_load, ask_gemini
import matplotlib.pyplot as plt
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

# Real PDF Generator Setup
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(question, answer):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor('#1E88E5'), spaceAfter=20)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#FFB300'), spaceBefore=15, spaceAfter=10)
    body_style = ParagraphStyle('Body', parent=styles['BodyText'], fontSize=11, leading=16, spaceAfter=10)
    story.append(Paragraph("AI Data Analytics - Executive Summary", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("User Query:", heading_style))
    story.append(Paragraph(question, body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Gemini AI Insights:", heading_style))
    story.append(Paragraph(answer.replace('\n', '<br/>'), body_style))
    doc.build(story)
    buffer.seek(0)
    return buffer

# --- DYNAMIC THEME ENGINE ---
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'dark'

st.sidebar.header("Theme Customization")
theme_choice = st.sidebar.radio("Select App Mode:", ["Dark Mode", "Light Mode"], 
                                index=0 if st.session_state['theme'] == 'dark' else 1)

if "Dark" in theme_choice:
    st.session_state['theme'] = 'dark'
    bg_color = "#121212"
    text_color = "#FFFFFF"
    card_bg = "#1E1E1E"
    plot_theme = 'dark_background'
else:
    st.session_state['theme'] = 'light'
    bg_color = "#F8F9FA"
    text_color = "#000000"
    card_bg = "#FFFFFF"
    plot_theme = 'default'

# 🌟 PREMIUM RESPONSIVE NAVBAR INTERACTIVE CSS (FIXED SIDEBAR OVERLAP)
st.markdown(f"""
    <style>
    /* Global Smooth Scroll Trigger */
    html, body, [data-testid="stAppViewContainer"] {{
        scroll-behavior: smooth !important;
        background-color: {bg_color};
        color: {text_color};
    }}
    
    /* Content Layer Layout Push */
    [data-testid="stMainBlockContainer"] {{
        padding-top: 130px !important;
    }}
    
    .main-title {{ font-size: 38px; font-weight: bold; color: #1E88E5; text-align: center; margin-bottom: 10px; }}
    
    /* 🌟 FIX: RESPONSIVE FLEXBOX NAVBAR CONTEXT (Chote Buttons Aur Left Sidebar Padding Offset) */
    .fixed-header-navbar {{
        position: fixed;
        top: 55px; 
        left: 0;
        width: 100%;
        background-color: {bg_color};
        z-index: 99999;
        padding: 25px 5% 12px 22%; /* Increased left padding (22%) to completely push buttons away from sidebar */
        border-bottom: 2px solid #1E88E5;
        box-shadow: 0px 6px 12px rgba(0,0,0,0.2);
        box-sizing: border-box;
    }}
    
    /* Responsive Flex Containers instead of Rigid Grid */
    .nav-button-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        width: 100%;
        max-width: 900px; /* Locks max width so buttons don't blow up */
    }}
    
    /* Premium Compact Button Styling */
    .nav-btn {{
        flex: 1;
        text-align: center;
        box-sizing: border-box;
        padding: 8px 4px; /* Reduced vertical & horizontal padding for smaller uniform sizes */
        background-color: #1E88E5;
        color: white !important;
        text-decoration: none !important;
        border-radius: 6px;
        font-weight: 600;
        font-size: 13px; /* Smaller font matrix */
        letter-spacing: 0.3px;
        white-space: nowrap; /* Forces text to stay in single line */
        transition: all 0.2s ease-in-out;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }}
    .nav-btn:hover {{
        background-color: #1565C0;
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(30, 136, 229, 0.3);
    }}
    .nav-btn:active {{
        transform: translateY(0);
        background-color: #0D47A1;
    }}
    
    /* Anchor Scroll Target Tuning Offset */
    div[id^="section-"] {{
        scroll-margin-top: 160px; 
    }}
    
    /* Streamlit Global Actions Buttons Overrides (Export & Analyze) */
    div.stButton > button {{
        width: 100% !important;
        background-color: #1E88E5 !important;
        color: white !important;
        border: none !important;
        padding: 10px 10px !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        font-size: 14px !important;
        transition: all 0.25s ease-in-out !important;
    }}
    div.stButton > button:hover {{
        background-color: #1565C0 !important;
    }}

    /* SCROLL REVEAL VIEW ANIMATION STYLES */
    .reveal-slide-up {{
        animation: revealSlideUp 0.8s cubic-bezier(0.25, 1, 0.5, 1) both;
    }}
    .reveal-zoom-in {{
        animation: revealZoomIn 0.8s cubic-bezier(0.25, 1, 0.5, 1) both;
    }}
    
    @keyframes revealSlideUp {{
        0% {{ opacity: 0; transform: translateY(30px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes revealZoomIn {{
        0% {{ opacity: 0; transform: scale(0.97) translateY(15px); }}
        100% {{ opacity: 1; transform: scale(1) translateY(0); }}
    }}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">Advanced AI Data Analytics Dashboard</div>', unsafe_allow_html=True)

# SIDEBAR CONTROLS
st.sidebar.markdown("---")
st.sidebar.header("Control Panel")

env_key_exists = os.getenv("GEMINI_API_KEY") is not None
user_api_key = None
if not env_key_exists:
    user_api_key = st.sidebar.text_input("Enter Your Gemini API Key", type="password")
    if not user_api_key:
        st.sidebar.warning("Live Mode Active: Provide API key to unlock AI Analytics.")
else:
    st.sidebar.success("Local Mode: Secure System API Key Loaded.")

uploaded_file = st.sidebar.file_uploader("Upload your Dataset (CSV format)", type=["csv"])

if uploaded_file is not None:
    try:
        with open("temp_dataset.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        df = clean_and_load("temp_dataset.csv")
        all_columns = list(df.columns)
        
        # 🌟 FIXED COMPACT NAVBAR HEADER WITH RIGHT SIDEBAR SHIFT
        st.markdown(f"""
            <div class="fixed-header-navbar">
                <div class="nav-button-container">
                    <a href="#section-preview" class="nav-btn">Preview Data</a>
                    <a href="#section-summary" class="nav-btn">Data Summary</a>
                    <a href="#section-viz" class="nav-btn">Visualization</a>
                    <a href="#section-ai" class="nav-btn">Analyze With AI</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 🌟 SECTION 1: PREVIEW DATA
        st.markdown('<div id="section-preview" class="reveal-slide-up">', unsafe_allow_html=True)
        st.subheader("Dataset Preview")
        st.dataframe(df, height=250, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br/><br/>", unsafe_allow_html=True)
        
        # 🌟 SECTION 2: DATA SUMMARY
        st.markdown('<div id="section-summary" class="reveal-zoom-in">', unsafe_allow_html=True)
        st.subheader("Automated Structural & Statistical Summary")
        
        c_rows, c_cols = st.columns(2)
        c_rows.metric("Total Rows", f"{len(df):,}")
        c_cols.metric("Total Columns", len(df.columns))
        
        summary_data = []
        for col in df.columns:
            summary_data.append({
                "Column Name": col,
                "Data Type": str(df[col].dtype),
                "Null Values": int(df[col].isnull().sum())
            })
        summary_df = pd.DataFrame(summary_data)
        st.markdown("**Column Meta Matrix (Types & Nulls):**")
        st.dataframe(summary_df, height=200, use_container_width=True)
        
        numeric_cols = df.select_dtypes(include=['number']).columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        
        if len(numeric_cols) > 0:
            st.markdown("**Numerical Profile:**")
            num_desc = df[numeric_cols].describe().loc[['count', 'mean', 'min', 'max']].T
            st.dataframe(num_desc, height=200, use_container_width=True)
            
        if len(categorical_cols) > 0:
            st.markdown("**Categorical Value Distribution:**")
            cat_choice = st.selectbox("Select Category Column to View Distribution:", categorical_cols)
            counts = df[cat_choice].value_counts().head(20)
            percentages = df[cat_choice].value_counts(normalize=True).head(20) * 100
            cat_distribution_df = pd.DataFrame({"Value Count": counts, "Percentage (%)": percentages.round(2).astype(str) + '%'})
            st.dataframe(cat_distribution_df, height=200, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br/><br/>", unsafe_allow_html=True)

        # 🌟 SECTION 3: CUSTOM VISUALIZATION ENGINE
        st.markdown('<div id="section-viz" class="reveal-slide-up">', unsafe_allow_html=True)
        st.subheader("Custom Visualization Engine")
        
        v_col1, v_col2 = st.columns([1, 1])
        with v_col1:
            chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram"])
            needs_y_axis = chart_type not in ["Pie Chart", "Histogram"]
            x_column = st.selectbox("Select X-Axis Column", all_columns)
            
            if needs_y_axis:
                y_column = st.selectbox("Select Y-Axis Column", all_columns, key="y_enabled")
            else:
                st.selectbox("Select Y-Axis Column (Not needed)", ["None / Disabled"], disabled=True, key="y_disabled")
                y_column = None
                
            custom_title = st.text_input("Chart Title", value=f"{chart_type} of {x_column}")
            custom_xlabel = st.text_input("X-Axis Label", value=x_column)
            custom_ylabel = st.text_input("Y-Axis Label", value=y_column if needs_y_axis else "Frequency / Value", disabled=not needs_y_axis)
            chart_color = st.color_picker("Pick Chart Theme Color", "#1E88E5")

        with v_col2:
            try:
                plt.style.use(plot_theme)
                fig, ax = plt.subplots(figsize=(6, 4))
                
                if chart_type == "Bar Chart":
                    df.groupby(x_column)[y_column].mean().head(15).plot(kind='bar', ax=ax, color=chart_color)
                elif chart_type == "Line Chart":
                    df.head(50).plot(kind='line', x=x_column, y=y_column, ax=ax, color=chart_color)
                elif chart_type == "Scatter Plot":
                    ax.scatter(df[x_column].head(100), df[y_column].head(100), color=chart_color, alpha=0.7)
                elif chart_type == "Pie Chart":
                    df[x_column].value_counts().head(5).plot(kind='pie', ax=ax, autopct='%1.1f%%')
                elif chart_type == "Histogram":
                    df[x_column].plot(kind='hist', ax=ax, bins=15, color=chart_color, edgecolor=text_color, alpha=0.8)
                
                ax.set_title(custom_title, color=text_color)
                ax.set_xlabel(custom_xlabel, color=text_color)
                ax.set_ylabel(custom_ylabel, color=text_color)
                fig.patch.set_facecolor(bg_color)
                ax.set_facecolor(card_bg)
                plt.tight_layout()
                st.pyplot(fig)
                
                buf = BytesIO()
                fig.savefig(buf, format="png", bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
                st.download_button(label="Export Custom Chart as PNG", data=buf.getvalue(), file_name=f"custom_{chart_type.lower()}.png", mime="image/png")
            except Exception as vis_err:
                st.error(f"Visualization Mismatch Error: {vis_err}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br/><br/>", unsafe_allow_html=True)

        # 🌟 SECTION 4: ASK GEMINI AI ABOUT DATA (FIXED FILTER BLOCK)
        st.markdown('<div id="section-ai" class="reveal-zoom-in">', unsafe_allow_html=True)
        st.subheader("Ask Gemini AI about Data")
        
        ai_col1, ai_col2 = st.columns([1, 1])
        with ai_col1:
            selected_ai_columns = st.multiselect(
                "Select specific Columns to send to AI Context:",
                options=all_columns,
                default=all_columns[:3] if len(all_columns) > 3 else all_columns
            )
            
            max_rows = len(df)
            rows_to_analyze = st.slider("Select rows to send to AI for Context:", min_value=5, max_value=min(max_rows, 500), value=min(max_rows, 20))
            user_question = st.text_input("Enter your query regarding the dataset:")
            
            has_access = env_key_exists or (user_api_key and user_api_key.strip() != "")
            
            if has_access:
                if st.button("Analyze with AI"):
                    if user_question:
                        with st.spinner("Gemini is thinking..."):
                            try:
                                # 🌟 FIX: Pehle dynamic dataframe columns filter kiya jo unexpected arg conflict solve karega
                                filtered_df = df[selected_ai_columns] if selected_ai_columns else df
                                
                                # Ab function ko bina selected_cols parameter ke safely execute kiya
                                answer = ask_gemini(filtered_df, user_question, custom_key=user_api_key, num_rows=rows_to_analyze)
                                
                                st.session_state['recent_q'] = user_question
                                st.session_state['recent_a'] = answer
                            except Exception as ai_err:
                                st.error(f"AI Error: API operational failure. Details: {ai_err}")
                    else:
                        st.warning("Please type a question first!")
            else:
                st.error("AI Feature Locked: Enter a valid Gemini API key in the sidebar.")

        with ai_col2:
            if 'recent_a' in st.session_state:
                st.success("AI Analysis Insights:")
                st.write(st.session_state['recent_a'])
                
                pdf_data = generate_pdf_report(st.session_state['recent_q'], st.session_state['recent_a'])
                st.download_button(label="Export Analysis as PDF", data=pdf_data, file_name="AI_Data_Analysis_Report.pdf", mime="application/pdf")
        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as general_err:
        st.error(f"File Parsing Error: {general_err}")
else:
    st.info("Welcome! Please configure settings from the sidebar and upload a data template.")