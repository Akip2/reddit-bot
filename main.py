import random
from communicator import generate_reply
from config import CLIENT_ID, PASSWORD, REDDIT_USERNAME, CLIENT_SECRET
import praw
import time
import datetime

# We only want to interact with extreme posts, either with an extremly positive or negative upvote ratio
MIN_POSITIVE_RATIO = 0.8 # Min ratio to interact with a "positive" post
MAX_NEGATIVE_RATIO = 0.3 # Max ratio to interact with a "negative" post
MIN_COMMENT_NB = 3

POST_LIMIT = None
COMMENT_LIMIT = 15

SUBS = [
    "AskReddit",
    "TodayILearned",
    "movies",
    "television",
    "gaming",
    "mildlyinteresting",
    "Showerthoughts",
    "NoStupidQuestions",
    "news",
    "socialanxiety"
]

def get_random_sub() -> str:
    return SUBS[random.randint(0, len(SUBS) - 1)]

def is_ratio_extreme(ratio: float) -> bool:
    return ratio >= MIN_POSITIVE_RATIO or ratio <= MAX_NEGATIVE_RATIO

def calculate_score(ratio: float, num_comments: int) -> float:
    if ratio >= MIN_POSITIVE_RATIO:
        return ratio * 10 + num_comments
    elif ratio <= MAX_NEGATIVE_RATIO:
        return (1 - ratio) * 10 + num_comments
    return 0

def treat_response(response: str) -> str:
    result = response
    if(response[0] == '"'):
        lastQuoteIndex = len(response) - (response[::-1].find('"') + 1)
        result = response[1:lastQuoteIndex]
        
    return result

def is_response_valid(response: str):
    return response.lower().find("i can't") != 0 and response.lower().find("i cannot") != 0

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    username=REDDIT_USERNAME,
    password=PASSWORD,
    user_agent='script:test-bot:v1.0 (by u/' + REDDIT_USERNAME + ')'
)

print("Connected as :", reddit.user.me())

while True: 
    sub_name = get_random_sub()
    subreddit = reddit.subreddit(sub_name)
    print("Target sub : "+sub_name)

    best_post = None
    best_score = 0
    for post in subreddit.new(limit=POST_LIMIT):
        if not post.is_self:
            continue
        
        ratio = post.upvote_ratio
        num_comments = post.num_comments
        
        if(is_ratio_extreme(ratio) and num_comments >= MIN_COMMENT_NB):
            positive = ratio >= MIN_POSITIVE_RATIO
                    
            score = calculate_score(ratio, num_comments) + random.randint(0, 200)
                
            if(score > best_score):
                best_score = score
                best_post = post
            
            break
                

    if(best_post != None):
        print("Target post :", best_post.title + " (" +best_post.url+")")
        response = treat_response(generate_reply(best_post.title, best_post.selftext, subreddit.display_name))
        
        if(is_response_valid(response)):
            print("\n💬 Answer generated :\n")
            print(response)
            best_post.reply(response)
            
            secondsBeforeNextComment = random.randint(600, 86400)
            future = datetime.datetime.now() + datetime.timedelta(seconds=secondsBeforeNextComment)
            print("Next action in : ")
            print(future)
            time.sleep(secondsBeforeNextComment)
    else:
        print("No interesting post found")
