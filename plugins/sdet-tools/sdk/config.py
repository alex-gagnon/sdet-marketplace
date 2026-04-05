"""Configuration loaded from environment variables."""
import os
from pathlib import Path

# Repository root — three levels up from this file (plugins/sdet-tools/sdk/)
REPO_ROOT = Path(__file__).resolve().parents[3]
TEMPLATES_DIR = REPO_ROOT / "plugins" / "sdet-tools" / "agents" / "test-generator"


class Config:
    jira_base_url: str = os.getenv("JIRA_BASE_URL", "")
    jira_email: str = os.getenv("JIRA_EMAIL", "")
    jira_api_token: str = os.getenv("JIRA_API_TOKEN", "")
    webhook_secret: str = os.getenv("WEBHOOK_SECRET", "")
    max_agent_turns: int = int(os.getenv("MAX_AGENT_TURNS", "25"))
    webhook_port: int = int(os.getenv("WEBHOOK_PORT", "8080"))


config = Config()
