import psycopg2

conn = psycopg2.connect(dbname="results18", user="dflvictory", password="dflguest18", host="dfl-election-returns.cmycsq7ldygm.us-east-2.rds.amazonaws.com")

cur = conn.cursor()

cur.execute("set time zone 'America/Chicago'")
cur.execute("INSERT INTO results18 (county, precinct, office, party, candidate, raw_votes, percent) values ('Yellow Medicine','ECHO TWP','Judge - 8th District Court 8','WRITE-IN**','WRITE-IN**',0,'0.00%')")

conn.commit()

cur.close()
conn.close()