# Imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# ✅ Set Page Config at the start
st.set_page_config(page_title="💿 Data Sweeper", layout="wide")

# Sidebar - Settings
with st.sidebar:
    st.header("⚙️ Settings")
    theme_choice = st.radio("Choose Theme:", ["Light", "Dark"])
    st.info("ℹ️ Use buttons below for quick actions.")
    st.button("🔄 Refresh Page")

# ✅ Inject Custom CSS for Themes
def set_theme(theme_choice):
    if theme_choice == "Dark":
        dark_theme_css = """
        <style>
        body { background-color: #1e1e1e !important; color: white !important; }
        .stApp { background-color: #1e1e1e !important; color: white !important; }
        .stButton>button { background-color: #4CAF50 !important; color: white !important; }
        .stRadio>div { color: white !important; }

        </style>
        """
        st.markdown(dark_theme_css, unsafe_allow_html=True)
    else:
        light_theme_css = """
        <style>
        body { background-color: white !important; color: black !important; }
        .stApp { background-color: white !important; color: black !important; }
        .stButton>button { background-color: #4CAF50 !important; color: black !important; }
        .stRadio>div { color: black !important; }
        h1, h2, h3, h4, h5, h6, p, label, .stAlert {
            color: black !important;
        }

        /* ✅ Header Bar Light Theme */
        header { background-color: #4CAF50 !important; }
        header * { color: black !important; }

        
        </style>
        """
        st.markdown(light_theme_css, unsafe_allow_html=True)

set_theme(theme_choice)  # ✅ Apply Theme


# App Title
st.markdown('<h1 style="color: #4CAF50;">💿 Data Sweeper</h1>', unsafe_allow_html=True)

st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

# File Uploader
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read file based on extension
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue  # Skip unsupported files
        
        # Display file details
        file_size_kb = len(file.getbuffer()) / 1024
        st.success(f"✅ File Loaded: {file.name} ({file_size_kb:.2f} KB)")

        # Show first 5 rows
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader(f"🛠️ Data Cleaning Options")

        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🚮 Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Removed Successfully!")

            with col2:
                if st.button(f"🔧 Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing Values Filled!")

        # Column Selection
        st.subheader("🎯 Choose Columns")
        columns = st.multiselect(f"Select Columns for {file.name}", df.columns, default=df.columns)    
        df = df[columns]

        # Data Visualization
        st.subheader("📊 Data Visualization") 
        if st.checkbox(f"Show Graph for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

        # Conversion Options
        st.subheader("🔁 Convert File Format")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"📥 Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"📥 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉🥳 All files processed successfully!")  


# ✅ Footer with credit
st.markdown('<p style="text-align: center; font-size: 16px; color: #4CAF50;">Made by Areeba Zafar 🚀</p>', unsafe_allow_html=True)