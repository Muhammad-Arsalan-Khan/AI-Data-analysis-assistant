# 📊 Advanced AI Data Analytics Dashboard

An automated, intelligent data analytics and visualization platform built with **Streamlit**, **Python**, and powered by the **Google Gemini AI** flagship models. This application allows users to upload raw CSV datasets, automatically generate interactive charts, and perform deep analytical Q&A using generative AI, with features to export reports directly as PDFs.

---

## 🚀 Features

- **💡 Automated Smart UI**: Clean dashboard layout optimized with dark mode themes.
- **📈 Dynamic Multi-Chart Engine**: Instantly switch between **Bar Charts, Line Charts, Scatter Plots,** and **Pie Charts** based on your dataset columns.
- **🤖 Gemini AI Integration**: Seamless natural language processing to query your data and receive accurate textual context summaries and answers.
- **📥 One-Click Export**:
  - Download dynamically generated charts as high-quality **PNG** images.
  - Export AI analysis summaries directly into a structured **PDF Report**.
- **🛡️ Secure Key & Error Handling**: Fully robust error mitigation utilizing `.env` configurations and structural `try-except` catchments preventing application crashes.

---

## 📁 Project Structure

```text
├── .env                  # Stores secure Google Gemini API keys
├── requirements.txt      # List of dependencies/libraries
├── main.py               # Application UI and Core Controller (Streamlit)
├── analysis.py           # Data cleansing and Gemini API integration
├── v.py                  # Automated background plotting configurations
└── README.md             # Project documentation (This file)
