import streamlit as st
import openai
from preprocessing import preprocess_text # Importing our custom-made preprocessing function
import SessionState

# Initialize session state
session_state = SessionState.get(api_key="", reviews=[])

# Select Page
page = st.sidebar.selectbox("Choose a page", ["Enter Review", "Analyze Reviews"])

# Page 1: Enter Review
if page == "Enter Review":
    st.header('Enter a new Review')

    # Input for New Review
    new_review = st.text_area("Enter your review here:")
    
    if st.button('Submit Review'):
        if new_review:
            session_state.reviews.append(new_review)
            st.success("Review Submitted Successfully!")
        else:
            st.warning("Please enter a review before submitting.")

# Page 2: View and Analyze Reviews
elif page == "Analyze Reviews":
    st.header('Analyze Reviews in Real-Time')

    # API Key Input
    if not session_state.api_key:
        session_state.api_key = st.text_input("Enter your OpenAI API Key:")
        if session_state.api_key:
            openai.api_key = session_state.api_key
    else:
        openai.api_key = session_state.api_key
    
    # If API key is set, display and analyze reviews
    if openai.api_key:
        if session_state.reviews:
            review = st.selectbox('Choose a review to analyze:', session_state.reviews)
            
            if st.button("Analyze Sentiment"):
                # Preprocess the review
                preprocessed_review = preprocess_text(review)

                # Analyze Sentiment
                response = openai.Completion.create(
                    engine="gpt-3.5-turbo",
                    prompt=f"The sentiment of this review is: {preprocessed_review}",
                    temperature=0.5,
                    max_tokens=100
                )
                st.write(response.choices[0].text.strip())
        else:
            st.info("No reviews have been submitted yet.")
    else:
        st.warning("You must enter your OpenAI API Key to use the app.")
