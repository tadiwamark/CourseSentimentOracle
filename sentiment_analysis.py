import openai
import pickle
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

# Load pre-fitted tokenizer
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
    
def load_uploaded_model(model_file, tokenizer_file):
    """Loads a model and tokenizer uploaded by the user."""
    with open(tokenizer_file, 'rb') as handle:
        tokenizer = pickle.load(handle)
    model = tf.keras.models.load_model(model_file)
    return model, tokenizer
    
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

def analyze_sentiment_simple(review_text, model=None, tokenizer=None):
    """Analyze sentiment using the provided model and tokenizer."""
    # If tokenizer is not provided, use the default one
    if tokenizer is None:
        with open('tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)

    # Use the default custom_model if no model is passed
    if model is None:
        model = custom_model
    """Sentiment Analysis."""
    preprocessed_text = preprocess_text(review_text)
    
    # Performing NLP using spaCy
    doc = nlp(preprocessed_text)

    # Extracting entities
    entities = [ent.text for ent in doc.ents]

    # Extracting keywords using noun chunks
    keywords = [chunk.text for chunk in doc.noun_chunks]

    # Analyzing sentiment using GPT 3.5 Turbo
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

         # Extracting keywords and entities using GPT 3.5 Turbo
        conversation = [
        {"role": "system", "content": "You are a helpful assistant. Provide sentiment, keywords, and entities separately."},
        {"role": "user", "content": f"For the review: '{preprocessed_text}', what is its sentiment? Also, list its keywords and entities."}
    ]

        response_keywords = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_keywords,
            temperature=0.5,
            max_tokens=150
        )

        response_content = response['choices'][0]['message']['content'].split('\n')

        # Assuming the model returns in the format "Sentiment: ...", "Keywords: ...", "Entities: ..."
        sentiment_result = response_content[0].replace("Sentiment:", "").strip()
        keywords = response_content[1].replace("Keywords:", "").split(',')
        entities = response_content[2].replace("Entities:", "").split(',')
    
        additional_features = {
            "keywords": [keyword.strip() for keyword in keywords],
            "entities": [entity.strip() for entity in entities]
        }
    
        return sentiment_result, additional_features

    except Exception as e:
        return str(e), None  # Returning error string and None for additional_features if there is an exception


def advanced_sentiment_analysis(review_text, model='gpt-3.5-turbo'):
    """
    Perform advanced sentiment analysis based on the selected model.

    Parameters:
    - review_text (str): The review text to analyze.
    - model (str): The model to use for analysis, either 'gpt-3.5-turbo' or 'simple'.

    Returns:
    - sentiment_result (str): The resulting sentiment.
    - additional_features (dict): Any additional features extracted, like entities or keywords.
    """

    if model == 'gpt-3.5-turbo':
        if openai.api_key:
            conversation = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"The sentiment of this review is: {review_text}"}
            ]
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=conversation,
                    temperature=0.5,
                    max_tokens=100
                )
                sentiment_result = response['choices'][0]['message']['content']
                
                
                additional_features = {
                    "keywords": [], 
                    "entities": []
                }
    
            except openai.error.OpenAIError as e:
                return str(e), None

    elif model == 'simple':
        # For the simple model, you'd process the review differently.
        sentiment_result ,additional_features = analyze_sentiment_simple(review_text)
        
    else:
        raise ValueError(f"Model {model} not supported.")

    return sentiment_result, additional_features


def additional_nlp_features(features):
    """Display additional NLP features."""
    if features:
        st.subheader("Extracted Keywords:")
        st.write(", ".join(features.get("keywords", [])))

        st.subheader("Recognized Entities:")
        st.write(", ".join(features.get("entities", [])))
