import os
from dotenv import load_dotenv, dotenv_values 
import praw

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
PASSWORD = os.getenv('PASSWORD')

assert CLIENT_ID, "CLIENT_ID missing"
assert CLIENT_SECRET, "CLIENT_SECRET missing"
assert REDDIT_USERNAME, "REDDIT_USERNAME missing"
assert PASSWORD, "PASSWORD missing"

MIN_RATIO = 0.5
LIMIT = 500
SUB = "socialanxiety"

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    username=REDDIT_USERNAME,
    password=PASSWORD,
    user_agent='script:test-bot:v1.0 (by u/' + REDDIT_USERNAME + ')'
)

print("Connected as :", reddit.user.me())

subreddit = reddit.subreddit(SUB)

for post in subreddit.new(limit=LIMIT):
    if(post.upvote_ratio >= MIN_RATIO):
        print(post.title)
        print(post.url)
        print(post.selftext)
        print("---------------")
