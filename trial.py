import psycopg2

conn = psycopg2.connect("postgresql://postgres:Thinkjs@localhost:5432/calcnexa")
print("Connection successful!")
conn.close()