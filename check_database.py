import sqlite3

conn = sqlite3.connect("data/mutual_funds.db")

result = conn.execute("PRAGMA integrity_check").fetchone()
print("Database:", result[0])

tables = conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()

print("Number of tables:", len(tables))
print("Table names:")

for table in tables:
    print("-", table[0])

conn.close()