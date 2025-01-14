from decouple import Config, RepositoryEnv

DOTENV_FILE = ".env"
env_config = Config(RepositoryEnv(DOTENV_FILE))

API_ID = int(env_config("API_ID"))
API_HASH = env_config("API_HASH")
BOT_TOKEN = env_config("BOT_TOKEN")
API_BASE_URL = env_config("API_BASE_URL")
SERVER_API_KEY = env_config("SERVER_API_KEY")
REDIS_HOST = env_config("REDIS_HOST")
REDIS_PORT = int(env_config("REDIS_PORT"))
REDIS_DB = int(env_config("REDIS_DB"))
