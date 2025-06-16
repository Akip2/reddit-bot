import os
from dotenv import load_dotenv
from communicator import generate_reply
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

# We only want to interact with extreme posts, either with an extremly positive or negative upvote ratio
MIN_POSITIVE_RATIO = 0.8 # Min ratio to interact with a "positive" post
MAX_NEGATIVE_RATIO = 0.3 # Max ratio to interact with a "negative" post
MIN_COMMENT_NB = 3

POST_LIMIT = 500
COMMENT_LIMIT = 15
SUB = "Advice"

def is_ratio_extreme(ratio):
    return ratio >= MIN_POSITIVE_RATIO or ratio <= MAX_NEGATIVE_RATIO

def calculate_score(ratio, num_comments):
    if ratio >= MIN_POSITIVE_RATIO:
        return ratio * 10 + num_comments
    elif ratio <= MAX_NEGATIVE_RATIO:
        return (1 - ratio) * 10 + num_comments
    return 0

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    username=REDDIT_USERNAME,
    password=PASSWORD,
    user_agent='script:test-bot:v1.0 (by u/' + REDDIT_USERNAME + ')'
)

print("Connected as :", reddit.user.me())

subreddit = reddit.subreddit(SUB)

best_post = None
best_score = 0
for post in subreddit.new(limit=POST_LIMIT):
    ratio = post.upvote_ratio
    num_comments = post.num_comments
    
    if(is_ratio_extreme(ratio) and num_comments >= MIN_COMMENT_NB):
        positive = ratio >= MIN_POSITIVE_RATIO
        score = 0
        
        score = calculate_score(ratio, num_comments)
            
        if(score > best_score):
            best_score = score
            best_post = post
            

if(best_post != None):
    print("Target post :", best_post.title + " (" +best_post.url+")")
    response = generate_reply(best_post.title, best_post.selftext, subreddit.display_name)
    print("\n💬 Answer generated :\n")
    print(response)
else:
    print("No interesting post found")
