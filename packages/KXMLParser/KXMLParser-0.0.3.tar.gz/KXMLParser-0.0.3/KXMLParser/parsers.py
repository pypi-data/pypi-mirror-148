"""
Provides XML parsing support.
"""

from rest_framework.parsers import BaseParser

import xmltodict
import json

class XMLParser(BaseParser):
    """
    XML parser.
    """

    media_type = "application/xml"

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream as XML and returns the resulting data.
        """
        xpars = xmltodict.parse(stream)
        json_par = json.dumps(xpars)
        json_par = json.loads(json_par) 

        return json_par
