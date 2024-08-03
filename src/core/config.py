import os

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "PwnsuprP6T45Qsbwywu2khUka!6IIlergPk!OFE35UP6n/QqeoED=iu/bUXBFY",
)
if not SECRET_KEY:
    SECRET_KEY = os.urandom(32)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 30
REFRESH_TOKEN_EXPIRES_MINUTES = 15 * 24 * 60  # 15 days


POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "root123")
POSTGRES_DB = os.getenv("POSTGRES_DB", "quantus")