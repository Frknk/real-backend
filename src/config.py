import os


def get_secret_key() -> str:
    return os.getenv("SECRET_KEY", "change-this-secret-key")


def get_algorithm() -> str:
    return os.getenv("ALGORITHM", "HS256")


def get_access_token_expire_minutes() -> int:
    raw_value = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    try:
        minutes = int(raw_value)
    except (TypeError, ValueError):
        return 30
    return minutes if minutes > 0 else 30


def get_allowed_origins() -> list[str]:
    raw_value = os.getenv("ALLOWED_ORIGIN", "*")
    if raw_value.strip() == "*":
        return ["*"]
    origins = [origin.strip() for origin in raw_value.split(",") if origin.strip()]
    return origins or ["*"]


def get_db_url() -> str:
    return os.getenv("DB_URL", "sqlite:///./app.db")


# Backward-compatible constants.
SECRET_KEY = get_secret_key()
ALGORITHM = get_algorithm()
ACCESS_TOKEN_EXPIRE_MINUTES = get_access_token_expire_minutes()
ALLOWED_ORIGIN = ",".join(get_allowed_origins())
DB_URL = get_db_url()
