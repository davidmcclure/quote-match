

import re
import shelve

from collections import defaultdict
from typing import List
from hirlite import Rlite
from vedis import Vedis
from boltons.iterutils import windowed_iter
from spooky import hash32
from bsddb3 import db


class BlastRlite:

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


class BlastVedis:

    def __init__(self, path: str):

        """
        Set the Vedis connection.
        """

        self.index = Vedis(path)

    def index_text(self, text: str, identifier: str, n: int):

        """
        Index N-grams for a text.
        """

        tokens = re.findall('[a-z]+', text.lower())

        for phrase in windowed_iter(tokens, n):

            key = hash32('.'.join(phrase))

            self.index.sadd(key, identifier)

    def lookup(self, ngram: List[str]):

        """
        Get text ids for an ngram.
        """

        key = hash32('.'.join(ngram))

        return self.index.smembers(key)


class BlastMem:

    def __init__(self):

        """
        Set the dictionary.
        """

        self.index = defaultdict(set)

    def index_text(self, text: str, identifier: str, n: int):

        """
        Index N-grams for a text.
        """

        tokens = re.findall('[a-z]+', text.lower())

        for phrase in windowed_iter(tokens, n):

            key = hash32('.'.join(phrase))

            self.index[key].add(identifier)

    def lookup(self, ngram: List[str]):

        """
        Get text ids for an ngram.
        """

        key = hash32('.'.join(ngram))

        return self.index.get(key)


class BlastShelve:

    def __init__(self, path: str):

        """
        Set the dictionary.
        """

        self.index = shelve.open(path)

    def index_text(self, text: str, identifier: str, n: int):

        """
        Index N-grams for a text.
        """

        tokens = re.findall('[a-z]+', text.lower())

        for phrase in windowed_iter(tokens, n):

            key = str(hash32('.'.join(phrase)))

            val = self.index.get(key, set())

            val.add(identifier)

            self.index[key] = val

    def lookup(self, ngram: List[str]):

        """
        Get text ids for an ngram.
        """

        key = str(hash32('.'.join(ngram)))

        return self.index.get(key)


class BlastBDB:

    def __init__(self, path: str):

        """
        Set the dictionary.
        """

        self.index = db.DB()

        self.index.open(path, None, db.DB_HASH, db.DB_CREATE)

    def add(self, text: str, identifier: str, n: int):

        """
        Index N-grams for a text.
        """

        tokens = re.findall('[a-z]+', text.lower())

        for phrase in windowed_iter(tokens, n):

            key = bytes(hash32('.'.join(phrase)))

            self.index.put(key, identifier)
