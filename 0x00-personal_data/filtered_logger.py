#!/usr/bin/env python3
"""Filters logging module"""
import logging
from typing import List
import re
from mysql.connector import MySQLConnection
import os

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


def get_logger() -> logging.Logger:
    """Returns a logging.Logger with RedactingFormatter as its formatter"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> MySQLConnection:
    """Returns a connector to the database"""
    cnx = MySQLConnection(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD"),
        host=os.getenv("PERSONAL_DATA_DB_HOST"),
        database=os.getenv("PERSONAL_DATA_DB_NAME"))

    return cnx


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
