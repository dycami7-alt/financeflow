from app.database import get_connection

conn = get_connection()
cursor = conn.cursor()

# Ver perfiles
cursor.execute('SELECT * FROM profiles')
profiles = cursor.fetchall()
print("Perfiles:")
for p in profiles:
    print(dict(p))

# Ver respuestas
cursor.execute('SELECT * FROM profile_answers')
answers = cursor.fetchall()
print("\nRespuestas:")
for a in answers:
    print(dict(a))

conn.close()