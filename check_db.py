import sqlite3
conn = sqlite3.connect('financeflow/financeflow.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tablas:', [t[0] for t in tables])
conn.close()