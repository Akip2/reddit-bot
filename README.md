# Reddit Comment Bot 🤖

A Reddit bot that scans posts in popular subreddits, generates replies using a language model API (Groq), and comments automatically on posts with extreme upvote ratios.

---

## 🔧 How It Works

1. Picks a random subreddit from a predefined list.
2. Looks for recent posts with **very high** or **very low** upvote ratios.
3. Uses a **language model API** (Groq or OpenAI-compatible) to generate a reply.
4. Posts that reply as a Reddit comment.
5. Waits a random amount of time before repeating.

---

## 📁 Project Structure

project\
├── main.py : Main Reddit interaction logic\
├── communicator.py : Handles API calls to the LLM\
├── config.py : Loads environment variables from .env\
├── requirements.txt : Python dependencies\
└── .env : Sensitive data (not tracked by Git)\

## 🔐 .env — Required Variables

Create a `.env` file in the project root:

```env
CLIENT_ID=your_reddit_app_client_id
CLIENT_SECRET=your_reddit_app_secret
REDDIT_USERNAME=your_reddit_username
PASSWORD=your_reddit_password
API_KEY=your_groq_api_key
```
---

## ▶️ How to Run the Bot

### 🖥️ Local Development

1. **Clone the repo**:
   ```bash
   git clone https://github.com/yourusername/reddit-bot.git
   cd reddit-bot
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
3. **Create your .env file (see section above for content).**
4. **Run the bot**:
   ```bash
   python main.py

