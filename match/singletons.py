

from .config import Config


config = Config.from_env()

stopwords = config.build_stopwords()
