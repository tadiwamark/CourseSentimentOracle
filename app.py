import streamlit as st
import openai
from preprocessing import preprocess_text  # Assume you have a separate module for preprocessing

# Initialize OpenAI API
openai.api_key = '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'

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
    
    # Sidebar with Information about the app and dataset
    st.sidebar.header('About App')
    st.sidebar.write('This app uses advanced NLP models to analyze sentiments of student reviews.')

    # User Input
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
            st.bar_chart({'Sentiment Score': {'Positive': 1 if 'positive' in result else 0, 'Negative': 1 if 'negative' in result else 0, 'Neutral': 1 if 'neutral' in result else 0}})
        else:
            st.warning('Please enter a review to analyze.')

if __name__ == "__main__":
    main()
