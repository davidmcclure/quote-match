

import re


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
