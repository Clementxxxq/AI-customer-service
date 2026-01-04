import sqlite3

DB_PATH = "clinic.db"

# 连接数据库
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# 执行 SQL 脚本
with open("create_tables.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

cur.executescript(sql_script)
conn.commit()
conn.close()

print("clinic.db created with sample data successfully!")
