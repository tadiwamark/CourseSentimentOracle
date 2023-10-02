import streamlit as st


def collect_feedback(user_input, sentiment_result, additional_features):
    """Collect user feedback on the sentiment analysis results and additional NLP features."""
    feedback = st.text_area("Provide feedback on the analysis:")
    if st.button("Submit Feedback"):
        if feedback:
            st.success("Thank you for your feedback!")
        else:
            st.warning("Feedback field is empty!")
