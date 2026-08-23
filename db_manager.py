import sqlite3
from datetime import date

# Initialize
db_filename = 'macro_data.db'
connection = sqlite3.connect(db_filename)
cursor = connection.cursor()

# Create macrodata table
create_macrodata = """CREATE TABLE IF NOT EXISTS
macro_data(id INTEGER PRIMARY KEY, data_name TEXT NOT NULL, stat_value REAL NOT NULL, source TEXT, series_key TEXT, stat_date TEXT NOT NULL, fetch_date TEXT NOT NULL)"""
cursor.execute(create_macrodata)
connection.commit()

# Fetch the entire table
def fetch_table():
    cursor.execute("SELECT * FROM macro_data")
    table = cursor.fetchall()
    return table

# Fetch a specific row in the table
def fetch_row(id):
    cursor.execute("SELECT * FROM macro_data WHERE id = ?",(id,))
    row = cursor.fetchone()
    return row

# Add a row to the table
def add_row(data_name,stat_value,stat_date,source=None,series_key=None):
    cursor.execute("""INSERT INTO macro_data 
    (data_name,stat_value,source,series_key,stat_date,fetch_date) 
    VALUES (?,?,?,?,?,?)""",(data_name,stat_value,source,series_key,stat_date,str(date.today())))
    connection.commit()
    return None