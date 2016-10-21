

import os
import anyconfig
import yaml

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.url import URL

from wordfreq import top_n_list


class Config:

    @classmethod
    def from_env(cls):

        """
        Get a config instance with the default files.
        """

        root = os.environ.get('MATCH_CONFIG', '~/.match')

        # Default paths.
        paths = [
            os.path.join(os.path.dirname(__file__), 'match.yml'),
            os.path.join(root, 'match.yml'),
        ]

        return cls(paths)

    def __init__(self, paths):

        """
        Initialize the configuration object.

        Args:
            paths (list): YAML paths, from most to least specific.
        """

        self.config = anyconfig.load(paths, ignore_missing=True)

    def __getitem__(self, key):

        """
        Get a configuration value.

        Args:
            key (str): The configuration key.

        Returns:
            The option value.
        """

        return self.config.get(key)

    def build_stopwords(self):

        """
        Get a set of whitelisted tokens.

        Returns: set
        """

        tokens = top_n_list('en', self['stopword_depth'], ascii_only=True)

        return set(tokens)
