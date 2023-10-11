import streamlit as st
import openai
import urllib.request
import tensorflow as tf
import SessionState  
from collections import deque
from sentiment_analysis import preprocess_text, analyze_sentiment_simple, load_uploaded_model, advanced_sentiment_analysis
from visualization import display_visualizations
from feedback import collect_feedback
from user_interface import show_instructions
import nltk


def main():
    st.title('Advanced NLP Course Sentiment Analysis App')

    # Get API Key for GPT-3.5
    if not st.session_state.get('api_key'):
        st.session_state.api_key = st.sidebar.text_input("Enter your OpenAI API Key:")
        if st.session_state.api_key:
            openai.api_key = st.session_state.api_key


    # Upload model and tokenizer
    uploaded_model = st.sidebar.file_uploader("Upload your custom model (.h5)", type=["h5"])
    uploaded_tokenizer = st.sidebar.file_uploader("Upload the tokenizer (.pickle)", type=["pickle"])

    # If both model and tokenizer are uploaded, load them.
    if uploaded_model and uploaded_tokenizer:
        custom_model, tokenizer = load_uploaded_model(uploaded_model, uploaded_tokenizer)
    else:
        st.sidebar.warning("To use the 'Uploaded Custom Model' option, you must upload both the model and the tokenizer.")


    # Define Page Layout
    st.sidebar.header('Navigation')
    page = st.sidebar.radio('Go to', ['Enter Review', 'Analysis', 'Advanced Analysis'])

    # Page logic.
    if page == 'Enter Review':
        st.title('Enter Your Review')

        user_input = st.text_area("Paste the course review here:")
        if st.button("Submit Review"):
            if user_input:
                if 'reviews' not in st.session_state:
                    st.session_state.reviews = deque(maxlen=100)
                st.session_state.reviews.appendleft(user_input)
                st.success("Review Submitted Successfully!")
            else:
                st.warning("Review field is empty!")

    elif page == 'Analysis':
            st.title('Real-time Review Analysis')
    
            model_choices = ['GPT-3.5 Turbo', 'Simple Model']
            if uploaded_model and uploaded_tokenizer:
                model_choices.append('Uploaded Custom Model')
            
            model_choice = st.selectbox('Choose a model', model_choices)
    
            if st.session_state.get('reviews'):
                selected_review_index = st.selectbox('Select a review to analyze:', list(range(len(st.session_state.reviews))), format_func=lambda x: st.session_state.reviews[x])
                selected_review = st.session_state.reviews[selected_review_index]
    
                if st.button("Analyze Review"):
                    sentiment = None  # initialize sentiment variable

                    if model_choice == 'GPT-3.5 Turbo':
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
                                sentiment = response['choices'][0]['message']['content']
                                st.write("GPT 3.5-Turbo's Response:", sentiment)
                            except openai.error.OpenAIError as e:
                                st.error(f"Error: {e}")
                        else:
                            st.error("OpenAI API Key is missing. Please enter the API Key.")
                
                    elif model_choice == 'Simple Model':
                        sentiment = analyze_sentiment_simple(selected_review)
                        st.write(f"Sentiment Analysis Result (using Simple Model): {sentiment}")
                
                    elif model_choice == 'Uploaded Custom Model':
                        sentiment = analyze_sentiment_simple(selected_review, custom_model, tokenizer)
                        st.write(f"Sentiment Analysis Result (using Uploaded Custom Model): {sentiment}")
                

    
            else:
                st.warning('No reviews have been submitted yet!')   

    elif page == 'Advanced Analysis':
        # Setup Instructions
        show_instructions()

        # User Input
        user_input = st.text_area("Enter the review:")
        if st.button('Analyze'):
            if user_input:
                # Sentiment Analysis
                sentiment_result, additional_features = advanced_sentiment_analysis(user_input)
                if additional_features:  # If no error occurred during sentiment analysis
                    st.success(f'Sentiment Analysis Result: {sentiment_result}')
                    additional_nlp_features(additional_features)
                    display_visualizations(sentiment_result, additional_features)
                    collect_feedback(user_input, sentiment_result, additional_features)
                else:
                    st.error(sentiment_result)  # Display error 
            else:
                st.warning('Please enter a review to analyze.')

    # Sidebar Information
    st.sidebar.header('About App')
    st.sidebar.write('This app allows users to enter course reviews and then analyzes the sentiment of the entered reviews in real-time using GPT-3.5 Turbo, a Simple Model, and additional advanced NLP techniques. You can even upload your own model and tokenizer!')

if __name__ == "__main__":
    main()
