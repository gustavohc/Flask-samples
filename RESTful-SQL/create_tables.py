import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)" #FOR PRIMARY KEYS YOU NEED TO ESPECIFY THE FULL TYPE NAME (INTERGER)
connection.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items(name text, price real)"
connection.execute(create_table)

connection.commit()
connection.close()
