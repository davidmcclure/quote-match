

import re

from difflib import SequenceMatcher

from match.singletons import stopwords


class Text:

    @classmethod
    def from_file(cls, path: str):

        """
        Read from a file.
        """

        with open(path) as fh:
            return cls(fh.read())

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

    def match(self, text):

        """
        Sequence match another text against this text.
        """

        s_tokens = self.token_sequence()
        q_tokens = text.token_sequence()

        matcher = SequenceMatcher(a=s_tokens, b=q_tokens)

        yield from matcher.get_matching_blocks()
