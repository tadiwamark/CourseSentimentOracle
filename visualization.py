import streamlit as st


def display_visualizations(sentiment_result, additional_features):
    """Display visualizations related to sentiment analysis and additional NLP features."""
    st.subheader("Sentiment Analysis Result:")
    st.write(sentiment_result)
    
