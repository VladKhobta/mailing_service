from envparse import Env

from pydantic import BaseSettings

env = Env()

REAL_DATABASE_URL = env.str(
    'REAL_DATABASE_URL',
    default='postgresql+asyncpg://postgres:postgres@host.docker.internal:5432/postgres'
)

TOKEN = env.str(
    "TOKEN"
)

APP_PORT = env.int(
    "APP_PORT",
    default=8000
)
