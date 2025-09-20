# pr_agent/config.py
import os

# Directory for cloning repositories temporarily
LOCAL_REPO_DIR = "temp_repo"

# Load environment variables (optional: if using .env)
from dotenv import load_dotenv
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
