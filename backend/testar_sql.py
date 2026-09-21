import sqlite3

cur = sqlite3.connect('bula_facil.db')
cursor = cur.cursor()

cursor.execute("SELECT * FROM medicamentos;")
results = cursor.fetchall()


cur.close()