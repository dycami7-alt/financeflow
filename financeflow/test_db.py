from app.database import get_connection

conn = get_connection()
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = [row[0] for row in cursor.fetchall()]
print("Tablas en la BD:", tables)
conn.close()