from typing import Optional
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    # App
    ENV: str = "dev"
    LOG_LEVEL: str = "INFO"

    # --- Project paths ---
    PROJECT_ROOT: Path = Path(__file__).resolve().parents[3]
    DATA_DIR: Path = PROJECT_ROOT / "data"
    DB_FILE: Path = DATA_DIR / "app.db"

    # --- placeholder so Pydantic knows this field exists ---
    DATABASE_URL: Optional[str] = None

    # --- Optional overrides ---
    SCHED_TZ: str = "America/Halifax"

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # --- Construct DATABASE_URL dynamically ---
    def __init__(self, **data):
        super().__init__(**data)
        # Always ensure data folder exists
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        # Build absolute DB URL
        self.DATABASE_URL = f"sqlite:///{self.DB_FILE}"


# Create global settings
settings = Settings()


class AppInfo(BaseModel):
    name: str = "fileshare-archiver-backend"
    version: str = "0.1.0"
    environment: str = settings.ENV


app_info = AppInfo()

# Debug prints
#print("🔍 [DEBUG] settings.DATABASE_URL =", settings.DATABASE_URL)
#print("🔍 [DEBUG] settings.DB_FILE =", settings.DB_FILE)
