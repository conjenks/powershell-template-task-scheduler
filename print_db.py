import sqlite3
import pandas as pd

conn = sqlite3.connect('jobs.db')
c = conn.cursor()

c.execute("SELECT * FROM jobs")

print("\nSCHEDULED JOBS\n------------------------------------------------")
print(pd.read_sql_query("SELECT * FROM jobs", conn))


for row in c:
    print(row[9])

# c.execute("DROP TABLE jobs")

conn.close()

