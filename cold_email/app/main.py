import streamlit as st

from chains import Chain
from utils import clean_text
from langchain_community.document_loaders import WebBaseLoader


def create_streamlit_app(llm, clean_text):
    st.title("Cold Email Generator")
    url_input = st.text_input("Enter the URL:", value="https://technopark.org/job-details/18627?job=DATA%20SCIENCE%20&%20AI/ML")
    portfolio_input = st.text_input("Your Portfolio Link:", value="https://yourportfolio.com"  # Default or leave empty
    )
    submit_button = st.button("Generate Email")
    
    if submit_button:
        try:
            loader= WebBaseLoader([url_input])
            data= clean_text(loader.load().pop().page_content)
            jobs= llm.extract_jobs(data)

            if len(jobs) == 0:
                st.error("No jobs found in the provided URL.")
            else:
                for job in jobs:
                    email = llm.generate_email(job, portfolio_input)
                    st.code(email, language="markdown")
        except Exception as e:
            st.error(f"An error occurred: {e}")



if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(page_title="Cold Email Generator", page_icon=":robot_face:", layout="wide")
    create_streamlit_app(chain, clean_text)
    
                    