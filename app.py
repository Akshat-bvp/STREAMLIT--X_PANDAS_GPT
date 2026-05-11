import streamlit as st 
import pandas_gpt as pg
from pandas_gpt.completers.openai import OpenAI
import pandas as pd

st.set_page_config(page_title="PandasGPT Explorer", layout="wide")
st.title('🔍 PANDAS_GPT DATA EXPLORER')

# Configure API in sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("API Key", type="password", placeholder="sk-...")
    
    if api_key:
        pg.completer = OpenAI(
            model="openai/gpt-4.1-nano",
            base_url="https://api.openai.com/v1",
            api_key=api_key
        )
        st.success("✅ API configured!")
    else:
        st.warning("⚠️ Please enter your API Key")

# Main content
url = st.text_input(
    '📊 Enter GitHub CSV link', 
    placeholder='https://raw.githubusercontent.com/username/repo/main/data.csv'
)

if url:
    try:
        df = pd.read_csv(url)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", df.shape[0])
        with col2:
            st.metric("Columns", df.shape[1])
        with col3:
            st.metric("Missing Values", df.isnull().sum().sum())
        
        with st.expander("📋 Data Preview", expanded=True):
            st.dataframe(df.head(10), width='stretch')  # ← FIXED
        
        st.markdown("---")
        st.subheader("🤖 Ask Questions")
        
        question = st.text_area(
            'Enter your question',
            placeholder='e.g., "Create plotly styled visualisations"',
            height=80
        )
        
        if question:
            with st.spinner("🔄 Analyzing..."):
                try:
                    result = df.ask(question)
                    st.success("✅ Complete!")
                    st.write(result)
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
    except Exception as e:
        st.error(f"❌ CSV Error: {str(e)}")
else:
    st.info("👉 Enter a GitHub CSV link to start!")
