# Database functions and utilities
import json
import os
import logging
logger = logging.getLogger(__name__)



class Database:
    def __init__(self, connection):
        self.connection = connection

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            return results
        except Exception as e:
            logger.error("Database query failed: %s", e)
            raise
        finally:
            cursor.close()
    
    def database_table_constructor(self):
        schema = json.load(open(os.path.abspath(os.path.dirname(__file__)) + "/database_schema.json"))
        cursor = self.connection.cursor()
        for table_name, table_def in schema.items():
            logger.debug("Ensuring table %s exists with definition: %s", table_name, table_def)
            columns_string = "("
            for column_name, column_type in table_def.items():
                columns_string += f"{column_name} {column_type},"
            columns_string = columns_string[:-1] + ");"
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} {columns_string}")
        cursor.close()