import streamlit as st
from sentiment_analysis import analyze_sentiment, analyze_sentiment_simple, additional_nlp_features

def main():
    st.title('Advanced NLP Course Sentiment Analysis App')
    
    # Define Page Layout
    st.sidebar.header('Navigation')
    page = st.sidebar.radio('Go to', ['Enter Review', 'Analysis'])

    # Model Choice
    model_choice = st.sidebar.selectbox("Choose a model", ["GPT-3.5 Turbo", "Custom Model"])

    # Page logic.
    if page == 'Enter Review':
        st.title('Enter Your Review')
        
        # User Input
        user_input = st.text_area("Paste the course review here:")
        
        if st.button("Submit Review"):
            if user_input:
                if model_choice == "GPT-3.5 Turbo":
                    sentiment_result, additional_features = analyze_sentiment(user_input)
                else:  # Custom Model
                    sentiment_result, additional_features = analyze_sentiment_simple(user_input)
                
                st.success(f'Sentiment Analysis Result: {sentiment_result}')
                additional_nlp_features(additional_features)

            else:
                st.warning("Review field is empty!")

    elif page == 'Analysis':
        # (This section remains the same as your previous code)

    # Sidebar Information
    st.sidebar.header('About App')
    st.sidebar.write('This app allows users to enter course reviews and then analyzes the sentiment using either GPT-3.5 Turbo or a custom model.')

if __name__ == "__main__":
    main()
