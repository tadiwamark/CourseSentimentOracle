# Course Sentiment Oracle

This repository hosts a sophisticated sentiment analysis application developed in Python using OpenAI's GPT-3.5 Turbo model. It performs real-time sentiment analysis on course reviews, providing immediate feedback and additional insights such as keyword extraction and entity recognition.

## Project contributors
### Tadiwanashe Nyaruwata R204445V
### Tungamirashe Mukwena R20

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Model Architecture](#model-architecture)
- [Project Structure](#project-structure)

## Introduction

Course Sentiment Oracle is designed to analyze the sentiment of user-submitted course reviews leveraging OpenAI's powerful NLP model. The application uses a combination of natural language processing and machine learning techniques to preprocess review texts and extract additional features, providing users with insightful and accurate analysis results.

## Installation

To set up and run the application, please follow the steps below:

1. Install the necessary libraries and dependencies:
   ```sh
   pip install openai streamlit nltk spacy
   ```

## Usage

1. **Web App**: Access the app at https://coursesentimentoracle.streamlit.app/

## Application Architecture

The application consists of two main components:
1. **Sentiment Analysis Model**: Leverages OpenAI's GPT-3.5 Turbo to analyze the sentiment of the preprocessed review text.
2. **Additional NLP Tasks**: Uses advanced NLP techniques to perform tasks like keyword extraction and entity recognition on the review text, providing additional insights.


## Project Structure

The project is organized into several key sections:
1. **Text Preprocessing**: Preprocesses user-inputted review text, including tasks like lowercasing and punctuation removal.
2. **Sentiment Analysis**: Analyzes the sentiment of the preprocessed text using OpenAI's model.
3. **Feature Extraction:**: Extracts additional features and insights from the text such as keywords and entities.
4. **Interface**: Presents an interactive Streamlit interface for users to input reviews and view analysis results.



