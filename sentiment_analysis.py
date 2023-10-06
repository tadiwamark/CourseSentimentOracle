import openai
import streamlit as st
import tensorflow as tf
from text_preprocessor import preprocess_text
import spacy
from collections import Counter

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Load custom model
CUSTOM_MODEL_PATH = "/content/drive/My Drive/Colab Notebooks/final_model.h5"
custom_model = tf.keras.models.load_model(CUSTOM_MODEL_PATH)

def analyze_sentiment(review_text):
    """Sentiment Analysis using GPT-3.5 Turbo."""
    preprocessed_text = preprocess_text(review_text)
    
    # Performing NLP using spaCy
    doc = nlp(preprocessed_text)

    # Extracting entities
    entities = [ent.text for ent in doc.ents]

    # Extracting keywords using noun chunks
    keywords = [chunk.text for chunk in doc.noun_chunks]

    # Analyzing sentiment using OpenAI
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
            "keywords": keywords,
            "entities": entities
        }
        
        return sentiment_result, additional_features

    except Exception as e:
        return str(e), None  # Returning error string and None for additional_features if there is an exception

def analyze_sentiment_simple(review_text):
    """Sentiment Analysis using the custom model."""
    preprocessed_text = preprocess_text(review_text)
    
    # Tokenization and padding
    tokenizer = Tokenizer(oov_token=OOV_TOKEN)
    sequence = tokenizer.texts_to_sequences([preprocessed_text])
    padded_sequence = pad_sequences(sequence, maxlen=MAX_LEN, padding=PADDING_TYPE, truncating=TRUNC_TYPE)
    
    # Making prediction
    prediction = custom_model.predict(padded_sequence)[0]
    
    if prediction >= 0.5:
        return "Positive", None
    else:
        return "Negative", None

def additional_nlp_features(features):
    """Display additional NLP features."""
    if features:
        st.subheader("Extracted Keywords:")
        st.write(", ".join(features.get("keywords", [])))

        st.subheader("Recognized Entities:")
        st.write(", ".join(features.get("entities", [])))
