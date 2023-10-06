import openai
import streamlit as st
import tensorflow as tf
from text_preprocessor import preprocess_text
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import spacy
from collections import Counter
import urllib.request

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Load custom model
def load_model_from_github(url):
    filename = url.split('/')[-1]
    urllib.request.urlretrieve(url, filename)
    loaded_model = tf.keras.models.load_model(filename)
    return loaded_model

# Download and Load Model
model_url = 'https://github.com/tadiwamark/CourseSentimentOracle/releases/download/sentiment-analysis/final_model.h5'
custom_model = load_model_from_github(model_url)

# Constants
MAX_LEN = 100
TRUNC_TYPE = 'post'
PADDING_TYPE = 'post'
OOV_TOKEN = "<OOV>"

# Tokenization
tokenizer = Tokenizer(oov_token=OOV_TOKEN)

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
    # Preprocess the review text
    preprocessed_text = preprocess_text(review_text)
    
    # If preprocess_text returned None or empty string
    if not preprocessed_text:
        return "Unable to process the review. It might be empty or not contain valid words."

    # Tokenize the preprocessed text
    sequence = tokenizer.texts_to_sequences([preprocessed_text])
    
    # Check if tokenizer returned an empty list
    if not sequence or not sequence[0]:
        return "Review contains words not seen during training. Unable to process."

    # Pad the sequence
    padded_sequence = pad_sequences(sequence, maxlen=MAX_LEN, padding=PADDING_TYPE, truncating=TRUNC_TYPE)
    
    # Predict the sentiment
    prediction = custom_model.predict(padded_sequence)

    # Convert prediction to sentiment label
    sentiment = "Positive" if prediction >= 0.5 else "Negative"

    return sentiment



def additional_nlp_features(features):
    """Display additional NLP features."""
    if features:
        st.subheader("Extracted Keywords:")
        st.write(", ".join(features.get("keywords", [])))

        st.subheader("Recognized Entities:")
        st.write(", ".join(features.get("entities", [])))
