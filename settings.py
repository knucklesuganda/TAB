import environs

env = environs.Env()
env.read_env('.env')

DATABASE_URL = env("DATABASE_URL")
BOT_KEY = env("BOT_KEY")
ADMINS_USERNAMES = tuple(env.list("ADMINS_IDS"))
DEBUG = env.bool('DEBUG')
