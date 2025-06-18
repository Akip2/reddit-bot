import subprocess

OLLAMA_MODEL = "myBot"

def generate_reply(post_title: str, post_body: str, subreddit: str) -> str:
    prompt = (
        f"The post is from r/{subreddit}.\n\n"
        f"Title: {post_title}\n\n"
        f"Text: {post_body}\n\n"
        f"Respond to the post. \n\n"
        f"Write only the body of your Reddit comment. No explanations, no disclaimers."
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
