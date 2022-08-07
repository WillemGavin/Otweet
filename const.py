import dotenv
import os
from pathlib import Path

current_dir = Path(__file__).parent.absolute()


# env_file = os.getenv("SCWEET_ENV_FILE", current_dir.parent.joinpath(".env"))
# dotenv.load_dotenv(env_file, verbose=True)


def load_env_variable(key, default_value=None, none_allowed=False):
    v = os.getenv(key, default=default_value)
    if v is None and not none_allowed:
        raise RuntimeError(f"{key} returned {v} but this is not allowed!")
    return v


def get_period(env):
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("PERIOD", none_allowed=True)


def get_write_mode(env):
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("WRITE_MODE", none_allowed=True)


def get_save_dir(env):
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("SAVE_DIR", none_allowed=True)

def get_from_account(env):
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("FROM_ACCOUNT", none_allowed=True)

def get_proxy(env):
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("PROXY", none_allowed=True)
