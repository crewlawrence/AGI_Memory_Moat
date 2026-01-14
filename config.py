"""Configuration helpers for the Prototype.

Provides a pydantic BaseSettings `Settings` class which reads configuration
from environment variables and an optional `.env` file. A module-level
`settings` instance is created for convenient import elsewhere in the codebase.

This file intentionally redacts sensitive values when printed.
"""
from __future__ import annotations

from dotenv import load_dotenv
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment or `.env`.

    Environment variables used (and their defaults):
    - FLASK_ENV: 'development'
    - FLASK_DEBUG: True
    - SECRET_KEY: 'change-me'
    - OPENAI_API_KEY: (optional)
    - CHROMA_PERSIST_DIRECTORY: 'chroma_persist'
    - DATABASE_URL: (optional)
    """

    flask_env: str = Field("development", env="FLASK_ENV")
    flask_debug: bool = Field(True, env="FLASK_DEBUG")
    # Do NOT hardcode secrets here. Use `.env` or environment variables.
    # Keep the default as None so secrets must be provided explicitly.
    secret_key: Optional[str] = Field(None, env="SECRET_KEY")
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    chroma_persist_directory: str = Field(
        "chroma_persist", env="CHROMA_PERSIST_DIRECTORY"
    )
    database_url: Optional[str] = Field(None, env="DATABASE_URL")

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }

    def as_safe_dict(self) -> dict:
        """Return a dict suitable for logging/printing with secrets redacted."""
        d = self.model_dump()
        if d.get("openai_api_key"):
            d["openai_api_key"] = "REDACTED"
        if d.get("secret_key"):
            d["secret_key"] = "REDACTED"
        return d

    def ensure_required(self) -> None:
        """Validate that required secrets are present in production.

        This intentionally does not try to 'fix' missing secrets. In
        production we want a visible failure so operators provide the
        appropriate secure values via environment variables or secrets
        management systems.
        """
        if self.flask_env.lower() == "production":
            missing = []
            if not self.secret_key:
                missing.append("SECRET_KEY")
            # Add other required secrets here as needed
            if missing:
                raise RuntimeError(
                    f"Missing required environment variables for production: {', '.join(missing)}"
                )


# Single shared settings instance
settings = Settings()


if __name__ == "__main__":
    # Quick local check that settings load (prints redacted values)
    import json

    print(json.dumps(settings.as_safe_dict(), indent=2))
