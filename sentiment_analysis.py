import openai
from text_preprocessor import preprocess_text
import nltk
import streamlit as st


def analyze_sentiment(review_text):
    """Sentiment Analysis."""
    preprocessed_text = preprocess_text(review_text)  # preprocess text before analysis
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"The sentiment of this review is: {preprocessed_text}"}
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            temperature=0.5,
            max_tokens=100
        )
        sentiment_result = response['choices'][0]['message']['content']

        # Additional NLP Tasks and Features extraction
        additional_features = {
            "keywords": ["Example", "Keyword"],
            "entities": ["Example", "Entity"]
        }

        return sentiment_result, additional_features
    except Exception as e:
        return str(e), None  # Returning error string and None for additional_features if there is an exception

def additional_nlp_features(features):
    """Display additional NLP features."""
    st.subheader("Extracted Keywords:")
    st.write(", ".join(features.get("keywords", [])))

    st.subheader("Recognized Entities:")
    st.write(", ".join(features.get("entities", [])))
