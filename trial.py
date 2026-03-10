import psycopg2

conn = psycopg2.connect("postgresql://postgres:12345678@localhost:5432/calcnexa")
print("Connection successful!")
conn.close()