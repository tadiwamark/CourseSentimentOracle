import streamlit as st

def setup_ui_elements():
    st.sidebar.header('About App')
    st.sidebar.write('This app uses advanced NLP models to analyze sentiments of student reviews.')

def show_instructions():
    st.info("Instructions: Enter a course review in the text area and click on 'Analyze' to get the sentiment analysis and additional insights.")
import streamlit as st



