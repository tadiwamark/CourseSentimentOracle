import streamlit as st
import openai
import SessionState  # Ensure you've implemented the session state.

# Create a session state for storing reviews.
session_state = SessionState.get(api_key="", reviews=[])

# Check if the API key is stored in the session state.
if not session_state.api_key:
    # Prompt the user to enter their OpenAI API key.
    session_state.api_key = st.sidebar.text_input("Enter your OpenAI API Key:")
    if session_state.api_key:
        # Set the API key for OpenAI.
        openai.api_key = session_state.api_key
else:
    openai.api_key = session_state.api_key

# Layout for page navigation.
st.sidebar.header('Navigation')
page = st.sidebar.radio('Choose a Page:', ['Enter Review', 'Analysis'])

# Page Logic.
if page == 'Enter Review':
    st.title('Enter Your Review')
    
    user_input = st.text_area("Paste the course review here:")

    if st.button("Submit Review"):
        # Store the review in session state.
        session_state.reviews.append(user_input)
        st.success("Review Submitted Successfully!")

elif page == 'Analysis':
    st.title('Real-time Review Analysis')

    # List the stored reviews.
    if session_state.reviews:
        selected_review = st.selectbox('Select a review to analyze:', session_state.reviews)

        if st.button("Analyze Review"):
            response = openai.Completion.create(
                engine="gpt-3.5-turbo",
                prompt=f"This is a review: '{selected_review}'. The sentiment of this review is:",
                temperature=0.5,
                max_tokens=100
            )
            st.write(response.choices[0].text.strip())
    else:
        st.warning('No reviews have been submitted yet!')

# Footer with instructions.
st.sidebar.text("\n")
st.sidebar.text("Instructions:")
st.sidebar.text("1. Navigate to 'Enter Review' to submit a review.")
st.sidebar.text("2. Switch to 'Analysis' to analyze the sentiment of entered reviews.")
st.sidebar.text("3. Reviews entered are stored only for the current session.")
