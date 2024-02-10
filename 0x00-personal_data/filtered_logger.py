#!/usr/bin/env python3
"""Filters logging module"""
import logging
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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum"""
        return filter_datum(
            self.fields, self.REDACTION,
            super(RedactingFormatter, self).format(record), self.SEPARATOR)
