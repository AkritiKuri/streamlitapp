import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
import os
import plotly.express as px

# 🌼 Streamlit page settings
st.set_page_config(page_title="🌸 Ingestion App", page_icon="🌺")
st.title("🌸 CSV Ingestion & Summary Report Generator 🌸")

# 🌷 Upload CSV
uploaded_file = st.file_uploader("🌼 Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("🌷 File uploaded successfully!")
    st.write("💐 Here's a preview of your data:")
    st.dataframe(df.head())

    # 🌼 Save to SQLite
    engine = create_engine("sqlite:///data.db")
    df.to_sql("ingested_data", con=engine, index=False, if_exists='replace')
    st.info("🪻 Data saved to database!")

    # 🌺 Option box for report or charts
    option = st.selectbox("🌸 What would you like to view?", ["Data Summary", "Charts"])

    if option == "Data Summary":
        summary = df.describe(include='all').fillna("N/A")
        st.subheader("📋 Summary Statistics")
        st.dataframe(summary)

        # 📄 Generate PDF
        if st.button("📄 Generate  PDF Report"):
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            c = canvas.Canvas(temp.name, pagesize=letter)
            width, height = letter
            text = c.beginText(40, height - 50)
            text.setFont("Helvetica", 10)
            text.textLine("🌸 Cute Summary Report 🌸")
            text.textLine("-" * 40)

            for column in summary.columns:
                text.textLine(f"🌼 Column: {column}")
                for stat, val in summary[column].items():
                    text.textLine(f"   {stat}: {val}")
                text.textLine("")

            c.drawText(text)
            c.save()

            with open(temp.name, "rb") as f:
                st.download_button("📥 Download Summary PDF", f, file_name="cute_summary_report.pdf")
            os.remove(temp.name)

    elif option == "Charts":
        st.subheader("📊 Bar Chart Garden 🌻")

        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        if len(numeric_columns) >= 1:
            selected_col = st.selectbox("🌸 Choose a column for bar chart", numeric_columns)

            bar_data = df[selected_col].value_counts().reset_index()
            bar_data.columns = [selected_col, "Count"]

            fig = px.bar(bar_data, x=selected_col, y="Count", title=f"🌼 Bar Chart of {selected_col}", color=selected_col)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("🌻 No numeric columns found to create a chart.")


