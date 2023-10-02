import streamlit as st
import openai
from preprocessing import preprocess_text  # Importing our custom mdae preprocessing function
import SessionState

# Initialize SessionState
session_state = SessionState.get(api_key="")

if not session_state.api_key:
    # Prompt the user to enter their OpenAI API key
    session_state.api_key = st.text_input("Enter your OpenAI API Key:")
    if session_state.api_key:
        # Set the API key for OpenAI
        openai.api_key = session_state.api_key
else:
    openai.api_key = session_state.api_key

def analyze_sentiment(text):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"This is a review: {text}. The sentiment of this review is:",
        temperature=0,
        max_tokens=60
    )
    return response.choices[0].text.strip()

def main():
    st.title('Advanced NLP Sentiment Analysis App')
    st.sidebar.header('About App')
    st.sidebar.write('This app uses advanced NLP models (GPT 3.5 Turbo) to analyze sentiments of student reviews.')

    if openai.api_key:
        user_input = st.text_area("Enter the review:")
        if st.button('Analyze'):
            if user_input:
                # Preprocess the input text
                preprocessed_text = preprocess_text(user_input)
                # Analyze Sentiment
                result = analyze_sentiment(preprocessed_text)
                # Display Result
                st.success(f'Sentiment Analysis Result: {result}')
                # Advanced Visualization of Result
                st.bar_chart({
                    'Sentiment Score': {
                        'Positive': 1 if 'positive' in result else 0,
                        'Negative': 1 if 'negative' in result else 0,
                        'Neutral': 1 if 'neutral' in result else 0
                    }
                })
            else:
                st.warning('Please enter a review to analyze.')
    else:
        st.warning("You must enter your OpenAI API Key to use the app.")

if __name__ == "__main__":
    main()
