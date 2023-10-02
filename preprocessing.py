import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download(['punkt', 'wordnet', 'stopwords'])

def preprocess_text(raw_text):
    """
    A function to preprocess text:
    - Lowercasing
    - Removal of Punctuation
    - Tokenization
    - Stopword Removal
    - Lemmatization
    """
    
    # Convert to lowercase
    text = raw_text.lower()
    
    # Remove Punctuation
    text = re.sub(f'[{string.punctuation}]', '', text)
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Stopword Removal
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    # Join tokens back to string
    text = ' '.join(tokens)
    
    return text
