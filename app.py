import streamlit as st 
import pandas_gpt as pg
from pandas_gpt.completers.openai import OpenAI
import pandas as pd

st.set_page_config(page_title="PandasGPT Explorer", layout="wide")
st.title('🔍 PANDAS_GPT DATA EXPLORER')

# Configure API from GitHub AI Models
try:
    api_key = st.secrets.get("GITHUB_AI_API_KEY", "")
    
    if not api_key:
        api_key = st.text_input("Enter GitHub AI API Key", type="password", placeholder="Your GitHub token")
    
    if api_key:
        pg.completer = OpenAI(
            model="openai/gpt-4.1-nano",
            base_url="https://models.github.ai/inference",
            api_key=api_key
        )
        st.success("✅ GitHub AI configured!")
    else:
        st.warning("⚠️ Please enter your GitHub AI API Key")
        st.stop()

except Exception as e:
    st.error(f"❌ Configuration error: {str(e)}")
    st.stop()

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
            st.dataframe(df.head(10), width='stretch')
        
        with st.expander("📊 Data Info"):
            st.write("**Data Types:**")
            st.write(df.dtypes)
            st.write("**Statistical Summary:**")
            st.write(df.describe())
        
        st.markdown("---")
        st.subheader("🤖 Ask Questions About Your Data")
        
        question = st.text_area(
            'Enter your question',
            placeholder='e.g., "Create plotly styled visualisations" or "Show me the top 5 rows"',
            height=80
        )
        
        if question:
            with st.spinner("🔄 Analyzing..."):
                try:
                    result = df.ask(question)
                    st.success("✅ Analysis Complete!")
                    st.markdown("### Result:")
                    st.write(result)
                    
                    # If result is a dataframe, allow download
                    if isinstance(result, pd.DataFrame):
                        csv = result.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Result as CSV",
                            data=csv,
                            file_name="analysis_result.csv",
                            mime="text/csv"
                        )
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
    except Exception as e:
        st.error(f"❌ CSV Error: {str(e)}")
else:
    st.info("👉 Enter a GitHub CSV link to start!")
