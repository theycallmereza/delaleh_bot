from decouple import Config, RepositoryEnv

DOTENV_FILE = ".env"
env_config = Config(RepositoryEnv(DOTENV_FILE))

API_ID = int(env_config("API_ID"))
API_HASH = env_config("API_HASH")
BOT_TOKEN = env_config("BOT_TOKEN")
