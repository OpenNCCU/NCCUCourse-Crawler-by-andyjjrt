import os
import sqlite3
import psycopg2
from psycopg2 import sql

from dotenv import load_dotenv

load_dotenv()


sqlite_conn = sqlite3.connect('data.db')
pg_conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)

pg_cursor = pg_conn.cursor()

sqlite_cursor = sqlite_conn.cursor()
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = sqlite_cursor.fetchall()

for table_name in tables:
    table_name = table_name[0]

    drop_table_query = sql.SQL(f"DROP TABLE IF EXISTS {table_name};")
    pg_cursor.execute(drop_table_query)

    # fetch schema
    sqlite_cursor.execute(f"PRAGMA table_info({table_name});")
    columns = sqlite_cursor.fetchall()

    #
    column_definitions = []
    for column in columns:
        col_name = column[1]
        col_type = column[2]

        # type projection
        if "INTEGER" in col_type:
            col_type = "INTEGER"
        elif "TEXT" in col_type:
            col_type = "TEXT"
        elif "REAL" in col_type:
            col_type = "DOUBLE PRECISION"
        elif "BLOB" in col_type:
            col_type = "BYTEA"
        else:
            col_type = "TEXT"

        column_definitions.append(f"{col_name} {col_type}")

    create_table_query = sql.SQL(
        f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_definitions)});"
    )
    pg_cursor.execute(create_table_query)

    # insert
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cursor.fetchall()
    for row in rows:
        placeholders = ', '.join(['%s'] * len(row))
        insert_query = sql.SQL(f"INSERT INTO {table_name} VALUES ({placeholders})ON CONFLICT DO NOTHING")
        pg_cursor.execute(insert_query, row)


pg_conn.commit()
sqlite_conn.close()
pg_cursor.close()
pg_conn.close()

print("migrate completed")