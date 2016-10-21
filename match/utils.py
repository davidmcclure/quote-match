

import re
import scandir


def scan_paths(root, pattern):

    """
    Walk a directory and gather up all file paths with a given extension.

    Args:
        root (str): The top-level directory.
        pattern (str): A filename regex.

    Yields: str
    """

    pattern = re.compile(pattern)

    for root, dirs, files in scandir.walk(root, followlinks=True):
        for name in files:

            # Match the extension.
            if pattern.search(name):
                yield os.path.join(root, name)
