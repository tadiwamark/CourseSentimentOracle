# app.py
import streamlit as st
from authentication import authenticate_user
from sentiment_analysis import analyze_sentiment, additional_nlp_features
from visualization import display_visualizations
from feedback import collect_feedback
from user_interface import setup_ui_elements, show_instructions

def main():
    st.title('Advanced NLP Sentiment Analysis App')
    
    # Authenticate User
    user = authenticate_user()  
    
    # Setup UI Elements and Instructions
    setup_ui_elements()
    show_instructions()
    
    # User Input
    user_input = st.text_area("Enter the review:")
    if st.button('Analyze'):
        if user_input:
            # Sentiment Analysis
            sentiment_result, additional_features = analyze_sentiment(user_input)
            st.success(f'Sentiment Analysis Result: {sentiment_result}')
            
            # Display Additional NLP Features
            additional_nlp_features(additional_features)
            
            # Display Visualizations
            display_visualizations(sentiment_result, additional_features)
            
            # Collect User Feedback
            collect_feedback(user_input, sentiment_result, additional_features)
        else:
            st.warning('Please enter a review to analyze.')

if __name__ == "__main__":
    main()
