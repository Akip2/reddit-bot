import requests
from config import API_KEY


API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

def generate_reply(post_title, post_body, subreddit):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    system_prompt = (
        "You are an average guy in his 20s leaving comments to reddit posts"
    )
    
    user_message = (
        f"The post is from r/{subreddit}.\n\n"
        f"Title: {post_title}\n\n"
        f"Text: {post_body}\n\n"
        f"Respond to the post.\nWrite only the body of your Reddit comment."
    )
    
    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "temperature": 1.7,
        "top_p": 0.95,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    }
    
    response = requests.post(API_URL, headers=headers, json=data)
    response.raise_for_status()
    completion = response.json()
    return completion["choices"][0]["message"]["content"]

# Exemple d'appel
if __name__ == "__main__":
    reply = generate_reply(
        "Why don't billionaires just retire?",
        "I always wonder why billionaires keep working.",
        "NoStupidQuestions"
    )
    print(reply)