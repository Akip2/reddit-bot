from attitude_enum import Attitude

import subprocess

OLLAMA_MODEL = "myBot"

def get_attitude_prompt(attitude: int):
    if(attitude == Attitude.NEGATIVE):
        return "Be brief and try to ragebait its author"
    elif(attitude == Attitude.POSITIVE):
        return "Be positive and supportive of its author"
    else:
        return ""

def generate_reply(post_title: str, post_body: str, subreddit: str, attitude: int) -> str:
    prompt = (
        f"Here is a reddit post in r/{subreddit} :\n\n"
        f"Title : {post_title}\n\n"
        f"Text : {post_body}\n\n"
        f"Answer. "+get_attitude_prompt(attitude)+"\n\n"
        f"Write only the content of the comment"
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
