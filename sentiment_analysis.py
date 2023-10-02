import openai
from text_preprocessor import preprocess_text
import nltk


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
     except openai.error.OpenAIError as e:
         return f"Error: {e}", None


def additional_nlp_features(features):
    """Display additional NLP features."""
    st.subheader("Extracted Keywords:")
    st.write(", ".join(features.get("keywords", [])))
    
    st.subheader("Recognized Entities:")
    st.write(", ".join(features.get("entities", [])))
