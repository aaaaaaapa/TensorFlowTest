import sqlite3

db_name='stockSub.db'
def creat_db():
    # 连接到数据库（如果不存在则会被创建）
    conn = sqlite3.connect(db_name)

    # 创建一个指向数据库的光标
    cursor = conn.cursor()

    # 创建一个名为 "users" 的表
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY,mastername TEXT, name TEXT,fundaccount INT,pwd TEXT)''')

    # 向表中插入一些数据
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','赵子范',540720097007,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','张圣彬',540630273482,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','张　明',540960143049,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','张广连',540620251925,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','严　艳',541300256815,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','严林燕',540620206907,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','严汉清',540820042641,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','严汉平',541300261829,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','严汉美',541400330710,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','严汉俊',541300262117,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','严　冲',541330160407,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','徐凡玮',540630210281,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','吴　云',540620211052,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','吴秀云',540730042220,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','吴小国',540620272449,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','吴声华',540620272511,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','吴茂和',540750012077,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','吴国琪',540940268398,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','束克珍',540820050046,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','刘小燕',540920006060,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','刘卫康',541300272430,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','刘王跃',540340008253,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','刘火华',540940286231,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','刘国云',540740068672,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','刘国进',541330051647,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','刘国芳',540820043453,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','刘国兵',541400330686,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','刘飞飞',540740089735,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','林　雨',540820033688,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','李鹏飞',540720046756,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','李　美',540940268392,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','李良芬',540820026213,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','姜卫平',540730042428,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','季　云',540940247491,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','季瑞成',540620270353,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','季凤才',540350133403,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','季曹连',540730026440,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','顾美琴',540760280318,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','顾丙元',540720099975,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','顾丙贤',540720099906,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','葛永明',540820133819,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','陈美娣',540760231170,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','陈百威',540760262530,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','曹永美',540730132272,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','曹永康',540820133225,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','曹雪云',540340008243,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','曹卫兰',540340008251,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','曹　平',540740255447,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','曹　建',540730102221,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YF','赵　雪',540830129503,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YM','季国标',540630213829,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YM','吴美琴',540660240248,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YM','吴国江',540940207257,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YM','胡荣花',540940207255,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YM','吴国平',540630207231,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YM','陆　飞',540630212507,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YM','曹建明',540940273751,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YM','吴陈伟',540320049909,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YM','胡美珍',540630266563,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YM','曹淑兰',540330223526,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YM','陆　莹',540660138295,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YM','胡永兵',540620210475,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YM','胡永兴',540660033243,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YM','吴美芳',540360265048,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YM','姜美琴',540630207233,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YM','胡宇敏',540360252071,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YM','陆福冲',540620210445,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YM','曹美群',540320047658,'623392')")
    cursor.execute("INSERT INTO users (mastername,name,fundaccount,pwd) VALUES ('YM','胡美琴',540660250649,'623392')")

    # 提交更改并关闭连接
    conn.commit()
    conn.close()

def query_db():

    # 连接到数据库
    conn = sqlite3.connect(db_name)

    # 创建一个指向数据库的光标
    cursor = conn.cursor()

    # 查询所有用户数据
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    # 获取列名信息
    columns = [column[0] for column in cursor.description]
    # 将行数据转换为字典列表
    result = []
    for row in rows:
        result.append(dict(zip(columns, row)))
    # 打印查询结果
    # for row in result:
    #     print(row)

    # 关闭连接
    conn.close()
    return result

# creat_db()
# query_db()