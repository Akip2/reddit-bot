# nathan.py

import subprocess

OLLAMA_MODEL = "adrian"

def generate_reply(post_title: str, post_body: str, subreddit: str) -> str:
    prompt = (
        f"Here is a reddit post in r/{subreddit} :\n\n"
        f"Title : {post_title}\n\n"
        f"Text : {post_body}\n\n"
        f"Answer to it"
    )

    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL, prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Ollama error :", e.stderr)
