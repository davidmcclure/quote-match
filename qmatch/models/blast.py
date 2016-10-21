

import re

from boltons.iterutils import windowed_iter
from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint
from spooky import hash32
from wordfreq import top_n_list

from qmatch.models import Base
from qmatch.singletons import session


class Blast(Base):

    __tablename__ = 'blast'

    __table_args__ = (
        PrimaryKeyConstraint('ngram', 'text'),
    )

    ngram = Column(Integer, nullable=False)

    text = Column(String, nullable=False)


class BlastIndexer:

    def __init__(self):
        self.cache = []
        self.tokens = set(top_n_list('en', 100))

    def add(self, text: str, identifier: str, n: int=4):

        """
        Index a text
        """

        tokens = [
            t for t in re.findall('[a-z]+', text.lower())
            if t not in self.tokens
        ]

        ngrams = set([
            hash32('.'.join(phrase))
            for phrase in windowed_iter(tokens, n)
        ])

        mappings = [
            dict(ngram=ngram, text=identifier)
            for ngram in ngrams
        ]

        self.cache += mappings

        if len(self.cache) > 1e6:
            self.flush()

    def flush(self):

        """
        Flush the cache to disk.
        """

        session.bulk_insert_mappings(Blast, self.cache)

        session.commit()

        self.cache.clear()
