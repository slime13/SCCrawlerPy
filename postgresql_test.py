import psycopg2

print('psycopg2 install test.')

conn = psycopg2.connect(database="dsidb", user="postgres", password="developer#!", host="121.129.214.6", port="8432")

print(conn)