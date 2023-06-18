import sqlite3

def creat_db():
    # 连接到数据库（如果不存在则会被创建）
    conn = sqlite3.connect('example.db')

    # 创建一个指向数据库的光标
    cursor = conn.cursor()

    # 创建一个名为 "users" 的表
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY, name TEXT,fundaccount INT,pwd TEXT)''')

    # 向表中插入一些数据
    cursor.execute("INSERT INTO users (name,fundaccount,pwd) VALUES ('Alice',12345678,'123456')")
    cursor.execute("INSERT INTO users (name,fundaccount,pwd) VALUES ('Bob',12345678,'123456')")
    cursor.execute("INSERT INTO users (name,fundaccount,pwd) VALUES ('Charlie',12345678,'123456')")

    # 提交更改并关闭连接
    conn.commit()
    conn.close()

def query_db():
    # 连接到数据库
    conn = sqlite3.connect('example.db')

    # 创建一个指向数据库的光标
    cursor = conn.cursor()

    # 查询所有用户数据
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    # 打印查询结果
    for row in rows:
        print(row)

    # 关闭连接
    conn.close()


creat_db()
query_db()