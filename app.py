import streamlit as st
import openai
import SessionState  
from collections import deque
#from authentication import authenticate_user
from sentiment_analysis import analyze_sentiment, additional_nlp_features
from visualization import display_visualizations
from feedback import collect_feedback
from user_interface import setup_ui_elements, show_instructions
import nltk

def main():
    st.title('Advanced NLP Course Sentiment Analysis App')
    
    # Authenticate User
    #user = authenticate_user()
    
    # Initialize Session State
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    if 'reviews' not in st.session_state:
        st.session_state.reviews = deque(maxlen=100)
    
    # Get API Key
    if not st.session_state.api_key:
        st.session_state.api_key = st.sidebar.text_input("Enter your OpenAI API Key:")
        if st.session_state.api_key:
            openai.api_key = st.session_state.api_key
    else:
        openai.api_key = st.session_state.api_key

    # Define Page Layout
    st.sidebar.header('Navigation')
    page = st.sidebar.radio('Go to', ['Enter Review', 'Analysis', 'Advanced Analysis'])

    # Page logic.
    if page == 'Enter Review':
        st.title('Enter Your Review')
        
        # User Input
        user_input = st.text_area("Paste the course review here:")
        if st.button("Submit Review"):
            if user_input:  # Prevent empty strings from being added
                st.session_state.reviews.appendleft(user_input)
                st.success("Review Submitted Successfully!")
            else:
                st.warning("Review field is empty!")
    
    elif page == 'Analysis':
        st.title('Real-time Review Analysis')
        
        if st.session_state.reviews:
            selected_review_index = st.selectbox('Select a review to analyze:', list(range(len(st.session_state.reviews))), format_func=lambda x: st.session_state.reviews[x])
            selected_review = st.session_state.reviews[selected_review_index]
            
            if st.button("Analyze Review"):
                if openai.api_key:
                    conversation = [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"The sentiment of this review is: {selected_review}"}
                    ]
                    
                    try:
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=conversation,
                            temperature=0.5,
                            max_tokens=100
                        )
                        st.write("GPT 3.5-Turbo's Response:", response['choices'][0]['message']['content'])
                    except openai.error.OpenAIError as e:
                        st.error(f"Error: {e}")
                else:
                    st.error("OpenAI API Key is missing. Please enter the API Key.")
        else:
            st.warning('No reviews have been submitted yet!')

        
    elif page == 'Advanced Analysis':
        # Setup UI Elements and Instructions
        setup_ui_elements()
        show_instructions()
            
        # User Input
        user_input = st.text_area("Enter the review:")
        if st.button('Analyze'):
            if user_input:
                # Sentiment Analysis
                sentiment_result, additional_features = analyze_sentiment(user_input)
                if additional_features:  # If no error occurred during sentiment analysis
                    st.success(f'Sentiment Analysis Result: {sentiment_result}')
                    additional_nlp_features(additional_features)
                    display_visualizations(sentiment_result, additional_features)
                    collect_feedback(user_input, sentiment_result, additional_features)
                else:
                    st.error(sentiment_result)  # Display error from analyze_sentiment
            else:
                st.warning('Please enter a review to analyze.')


    # Sidebar Information
    st.sidebar.header('About App')
    st.sidebar.write('This app allows users to enter course reviews and then analyzes the sentiment of the entered reviews in real-time using GPT-3.5 Turbo and additional advanced NLP techniques.')

if __name__ == "__main__":
    main()
