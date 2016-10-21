

import re
import bz2

from difflib import SequenceMatcher

from match.singletons import stopwords


class Text:

    @classmethod
    def from_txt(cls, path: str):

        """
        Read from a text file.
        """

        with open(path) as fh:
            return cls(fh.read())

    @classmethod
    def from_stacks(cls, path: str):

        """
        Read from a Stacks archive file.
        """

        with bz2.open(path, 'rt') as fh:

            text = json.loads(fh.read())

            return cls(text['plain_text'])

    def __init__(self, text: str):

        """
        Tokenize the text.
        """

        self.text = text

        self.tokens = [
            (m.group(0), m.start(), m.end())
            for m in re.finditer('[a-z]+', text.lower())
        ]

    def token_sequence(self):

        """
        Provide the raw sequence of tokens, without positions.
        """

        return [
            token for token, start, end in self.tokens
            if token not in stopwords
        ]

    def match(self, text, min_size: int=5):

        """
        Sequence match another text against this text.
        """

        s_tokens = self.token_sequence()
        q_tokens = text.token_sequence()

        matcher = SequenceMatcher(a=s_tokens, b=q_tokens)

        for match in matcher.get_matching_blocks():
            if match.size >= min_size:
                yield match
