# Course Sentiment Oracle

This repository hosts a sophisticated sentiment analysis application developed in Python using OpenAI's GPT-3.5 Turbo model. It performs real-time sentiment analysis on course reviews, providing immediate feedback and additional insights such as keyword extraction and entity recognition.

## Project contributors
### Tadiwanashe Nyaruwata R204445V
### Tungamirashe Mukwena R20

#### Access the app at [https://coursesentimentoracle.streamlit.app/](https://coursesentimentoracle.streamlit.app/)
#### Link to YouTube video that demonstrates how our app works 

## Table of Contents

- [Introduction](#introduction)
- [About the Dataset](#about-the-dataset)
- [Installation](#installation)
- [Usage](#usage)
- [Model Architecture](#model-architecture)
- [Why GPT Outperforms Our Model](#why-gpt-outperforms)
- [Project Structure](#project-structure)

## Introduction

Course Sentiment Oracle is designed to analyze the sentiment of user-submitted course reviews leveraging OpenAI's powerful NLP model and a custom trained model. The application uses a combination of natural language processing and machine learning techniques to preprocess review texts and extract additional features, providing users with insightful and accurate analysis results.

## About the Dataset

### Context
The dataset was scraped from the Coursera platform. The dataset's main challenge is its imbalanced nature.

### Content
The dataset contains two files: `reviews.csv` and `reviews_by_course.csv`. The `reviews.csv` file provides individual course reviews and their respective labels, while the `reviews_by_course.tsv` groups reviews by the `CourseId` column. We will be using the `reviews.csv` file.

#### reviews.csv Fields:
- `Id` - The unique identifier for a review.
- `Review` - The actual course review.
- `Label` - The sentiment label of the course review, categorized based on the course rating: Very Positive (5-star), Positive (4-star), Neutral (3-star), Negative (2-star), and Very Negative (1-star).

## Installation

To set up and run the application, follow the steps below:

1. **Clone the GitHub repository:**
    ```sh
    git clone https://github.com/tadiwamark/CourseSentimentOracle.git
    cd CourseSentimentOracle
    ```

2. **Install the necessary libraries and dependencies:**
    ```sh
    pip install openai streamlit nltk spacy tensorflow
    ```

3. **Start the Streamlit application:**
    ```sh
    streamlit run app.py
    ```

## Usage

**Web App:** Access the app at [https://coursesentimentoracle.streamlit.app/](https://coursesentimentoracle.streamlit.app/)

## Model Architecture

The application consists of two main components:

1. **Sentiment Analysis Model:** Uses OpenAI's GPT-3.5 Turbo and a custom-trained TensorFlow model to analyze the sentiment of the preprocessed review text.
2. **Additional NLP Tasks:** Employs advanced NLP techniques to perform tasks like keyword extraction and entity recognition, providing added insights.

## Why GPT Outperforms Our Model

OpenAI's GPT-3.5 Turbo model, as one of the most advanced language models, can generate human-like text based on the input it receives. Its vast pre-training data allows it to understand diverse contexts and linguistic nuances. In contrast, our custom model, though specialized, has been trained on a limited dataset. This makes GPT-3.5 Turbo better equipped to handle varied inputs and deliver more accurate sentiment analysis results.

## Project Structure

The project is structured into several crucial sections:

1. **Text Preprocessing:** Processes user-inputted review text, including tasks like lowercasing and punctuation removal.
2. **Sentiment Analysis:** Uses OpenAI's model and the custom model to assess the sentiment of the preprocessed text.
3. **Feature Extraction:** Gleans additional features and insights from the text, such as keywords and entities.
4. **Interface:** Offers an interactive Streamlit interface for users to input reviews and view analysis outcomes.

