import openai
import spacy
import RAKE

# Load SpaCy model
nlp = spacy.load('en_core_web_sm')

# Setup RAKE
rake = RAKE.Rake(RAKE.SmartStopList())

def analyze_sentiment(text):
    # Replace with actual OpenAI API call for Sentiment Analysis.
    response = openai.Completion.create(
        engine="gpt-3.5-turbo", 
        prompt=f"This is a review: {text}. The sentiment of this review is:", 
        temperature=0, 
        max_tokens=60
    )
    sentiment_result = response.choices[0].text.strip()
    
    # Extracting Keywords using RAKE
    extracted_keywords = [keyword[0] for keyword in rake.run(text, maxWords=3, minFrequency=2)]
    
    # Named Entity Recognition using SpaCy
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents]
    
    additional_features = {'keywords': extracted_keywords, 'entities': entities}
    return sentiment_result, additional_features
