from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4o-mini"  # change as desired
    ICP_INDUSTRIES: list = ["B2B SaaS"]  # default ICP list; can pass more via env if you like

    class Config:
        env_file = ".env"

settings = Settings()
