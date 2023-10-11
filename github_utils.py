import requests
import pandas as pd
import base64
import io

GITHUB_TOKEN = 'TGtCCVo288s674r7qMTacqARRVo0fUtDw8bBSgEzyLA'

def get_file_content():
    """Fetch the file content from GitHub repository"""
    url = f"https://github.com/tadiwamark/CourseSentimentOracle/blob/main/reviews_sentiments.csv"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.raw"
    }
    response = requests.get(url, headers=headers)
    print(response.text)
    csv_content = base64.b64decode(response.json()['content']).decode('utf-8')
    return csv_content

def update_github_file(new_content):
    """Commit the updated content back to the GitHub repository"""
    url = f"https://github.com/tadiwamark/CourseSentimentOracle/blob/main/reviews_sentiments.csv"
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
    print(response.text)
    response = requests.put(url, headers=headers, json=payload)
    
    return response

def append_to_csv_and_commit(review, sentiment, model):
    csv_content = get_file_content()
    df = pd.read_csv(io.StringIO(csv_content))
    new_data = pd.DataFrame({"review": [review], "sentiment": [sentiment], "model_used": [model]})
    df = df.append(new_data, ignore_index=True)
    new_csv_content = df.to_csv(index=False)
    update_github_file(new_csv_content)
