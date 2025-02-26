"""
A helper class to parse json data.
"""

import json
from re import findall


class JsonHelper():
    def __init__(self):
        pass

    def loads(self, content):
        """Parse json data from content.

        This method use regex `'({.*})'` to find the json data in the content. The regex means to find the first `{` and the last `}` in the content, and the content between them is the json data.

        If the content is bytes, it will be decoded to string first; if there is more than one json data in the content, only the first one will be parsed.
        
        Args:
            content (str):  The content to parse.

        Returns:
            result (dict):  The parsed json data.
        """
        result = {}
        try:
            if isinstance(content, bytes):
                content = bytes.decode(content)
            result = json.loads(findall(r'({.*})', content)[0])
        except Exception:
            print("Cannot parse the content as json data: %s" % content)
            exit(1)
        return result
