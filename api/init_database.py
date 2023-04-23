import os
import sqlite3


if __name__ == "__main__":
    if os.path.exists('example.db'):
        os.remove('example.db')
    with open('init_database.sql', 'r') as sql_file:
        script = sql_file.read()
    sqlite3.connect('example.db')
    connection = sqlite3.connect('example.db')
    cursor = connection.cursor()
    cursor.executescript(script)
    connection.commit()

