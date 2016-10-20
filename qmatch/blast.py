

import re

from typing import List
from hirlite import Rlite
from boltons.iterutils import windowed_iter
from spooky import hash32


class Blast:

    def __init__(self, path: str):

        """
        Set the Rlite connection.
        """

        self.index = Rlite(path)

    def index_text(self, text: str, identifier: str, n: int):

        """
        Index N-grams for a text.
        """

        tokens = re.findall('[a-z]+', text.lower())

        for phrase in windowed_iter(tokens, n):

            key = str(hash32('.'.join(phrase)))

            self.index.command('sadd', key, identifier)

    def lookup(self, ngram: List[str]):

        """
        Get text ids for an ngram.
        """

        key = str(hash32('.'.join(ngram)))

        return self.index.command('smembers', key)
