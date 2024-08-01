#!/usr/bin/env python3
""" Obfuscating specified fields in a log message """

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """ Obfuscation implementation """
    pattern = f"({'|'.join(fields)})=[^\\{separator}]+"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
