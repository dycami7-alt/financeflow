import os

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
CLAUDE_API_URL = os.getenv(
    "CLAUDE_API_URL",
    "https://api.anthropic.com/v1/complete"
)
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3.5")
CLAUDE_MAX_TOKENS = int(os.getenv("CLAUDE_MAX_TOKENS", "1000"))

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "financeflow.db")),
)

CHAT_RATE_LIMIT_PER_MINUTE = int(os.getenv("CHAT_RATE_LIMIT_PER_MINUTE", "5"))
CHAT_MAX_MESSAGE_LENGTH = int(os.getenv("CHAT_MAX_MESSAGE_LENGTH", "2000"))
