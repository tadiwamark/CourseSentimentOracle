import requests
import pandas as pd
import base64
import io

GITHUB_TOKEN = 'YOUR_GITHUB_TOKEN'
REPO_OWNER = 'tadiwamark'
REPO_NAME = 'CourseSentimentOracle'
FILE_PATH = 'reviews_sentiments.csv'

def get_file_content():
    """Fetch the file content from GitHub repository"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.raw"
    }
    response = requests.get(url, headers=headers)
    csv_content = base64.b64decode(response.json()['content']).decode('utf-8')
    return csv_content

def update_github_file(new_content):
    """Commit the updated content back to the GitHub repository"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
    }

    # Get sha of the current file
    sha = requests.get(url, headers=headers).json()['sha']

    # Encode new content to base64
    new_content_encoded = base64.b64encode(new_content.encode()).decode('utf-8')
    
    commit_message = "Update reviews_sentiments.csv with new data"
    payload = {
        "message": commit_message,
        "content": new_content_encoded,
        "sha": sha
    }
    response = requests.put(url, headers=headers, json=payload)
    return response

def append_to_csv_and_commit(review, sentiment, model):
    csv_content = get_file_content()
    df = pd.read_csv(io.StringIO(csv_content))
    new_data = pd.DataFrame({"review": [review], "sentiment": [sentiment], "model_used": [model]})
    df = df.append(new_data, ignore_index=True)
    new_csv_content = df.to_csv(index=False)
    update_github_file(new_csv_content)