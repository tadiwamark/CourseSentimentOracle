import openai
from text_preprocessor import preprocess_text


def analyze_sentiment(review_text):
    """Sentiment Analysis."""
    preprocessed_text = preprocess_text(review_text)  # preprocess text before analysis
    
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=f"This is a review: '{preprocessed_text}'. The sentiment of this review is:",
        temperature=0.5,
        max_tokens=100
    )
    sentiment_result = response.choices[0].text.strip() 
    
    # Additional NLP Tasks and Features extraction
    additional_features = {
        "keywords": ["Example", "Keyword"],
        "entities": ["Example", "Entity"]
    }
    
    return sentiment_result, additional_features


def additional_nlp_features(features):
    """Display additional NLP features."""
    st.subheader("Extracted Keywords:")
    st.write(", ".join(features.get("keywords", [])))
    
    st.subheader("Recognized Entities:")
    st.write(", ".join(features.get("entities", [])))
