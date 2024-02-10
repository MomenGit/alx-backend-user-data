#!/usr/bin/env python3
"""Filters logging module"""
from typing import List
import re


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """Returns the log message obfuscated
    Example:
    i/p: name=egg;password=eggcellent;date_of_birth=12/12/1986;
    o/p: name=egg;password=xxx;date_of_birth=xxx;
    """
    temp = message
    for field in fields:
        temp = re.sub(f"{field}=.*?{separator}",
                      f"{field}={redaction}{separator}", temp)
    return temp
