#!/usr/bin/env python3
""" function to filter logs """
from typing import List
import re
import logging
import os
import mysql.connector


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ constructor for redacting class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ formatter for redacting class """
        log = super().format(record)
        return filter_datum(self.fields, self.REDACTION, log, self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ filter data function for logs """
    for field in fields:
        pattern = f"(?<={field}=).*?(?={separator})"
        message = re.sub(pattern, redaction, message)
    return message


PII_FIELDS = ("ssn", "password", "phone", "email", "name")


def get_logger() -> logging.Logger:
    """ log getter function for filtration """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ get database """
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pass = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")

    cnx = mysql.connector.connect(host=db_host, port=3306,
                                  user=db_username, password=db_pass,
                                  database=db_name)
    return cnx


def main():
    """ main function for doing db stuff """
    cnx = get_db()
    cursor = cnx.cursor()
    query = ("SELECT * FROM users;")
    cursor.execute(query)
    logger = get_logger()
    for item in cursor:
        data = []
        for descr, it in zip(cursor.description, item):
            pii = f"{descr[0]}={str(it)}"
            data.append(pii)
        log_data = "; ".join(data)
        logger.info(log_data)
    cursor.close()
    cnx.close()


if __name__ == "__main__":
    main()
