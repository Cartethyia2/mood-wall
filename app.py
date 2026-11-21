# 心情墙后端 · 你的第一台服务器
# 运行方法：python app.py  （然后浏览器打开 http://127.0.0.1:5000/api/hello）

from flask import Flask, jsonify, request
from datetime import datetime
# app 就是"服务器本体"，所有功能都挂在它身上
app = Flask(__name__)
app.json.ensure_ascii = False  # JSON 里的中文别转义成 \uXXXX，原样输出

# @app.route(...) 是"门牌号"：
# 意思是——只要有浏览器来敲 /api/hello 这个门，就执行下面这个函数
@app.route("/api/hello")
def hello():
    # jsonify = 后端的"打包"：把 Python 字典变成 JSON 文本寄回给浏览器
    # （和你前端 JSON.parse 拆包正好相反，还记得吗）
    return jsonify({"msg": "你好，世界", "from": "你的第一台服务器"})




# ================= 数据库基建（今天的新仓库） =================
import sqlite3

def get_db():
    """打开数据库文件 mood.db（不存在会自动创建），返回连接。"""
    db = sqlite3.connect("mood.db")
    db.row_factory = sqlite3.Row   # 查出来的每行可以按列名取值，像字典一样
    return db

def init_db():
    """建表（如果还没有）。表 = 带列的清单，这张表叫 notes，有三列：name/text/time。"""
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            text TEXT,
            time TEXT
        )
    """)
    # 如果表是空的，放两张示例纸条
    count = db.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    if count == 0:
        db.execute("INSERT INTO notes (name, text, time) VALUES (?, ?, ?)",
                   ("小K", "今天广州下雨，适合摸头", "2026-11-14 18:00"))
        db.execute("INSERT INTO notes (name, text, time) VALUES (?, ?, ?)",
                   ("刳云", "后端课第一天，我居然在写服务器", "2026-11-14 18:01"))
    db.commit()   # 提交 = 落盘保存（和 git commit 的"落账"一个意思）
    db.close()

init_db()

@app.route("/api/notes")
def send_notes(): 
    db = get_db() #开门，db类似于一台仓库对讲机，这一行是领取对讲机
    rows = db.execute("SELECT name, text, time FROM notes").fetchall()#从notes里面选这些变量，db.execute(SQL) =把取货单交给仓库，仓库跑去找货，回来时推着一个小推车（装着找到的所有行）；.fetchall() = 把小推车上的货全部卸下来，变成一个列表；rows是一个名字
    db.close()#下班还对讲机
    return jsonify([dict(r) for r in rows])#r是一种特殊的包装，jsonify不会打这个包，要先变成普通字典。对 rows 里的每一个 r，都 dict(r) 一下，收成新列表"。然后 jsonify 打包寄回


@app.route("/api/notes",methods =["POST"]) 
def receive_notes(): 
    note=request.get_json() 
    note["time"] = datetime.now().strftime("%Y-%m-%d %H:%M")#盖章服务器官方时间
    db = get_db()#跟55一样
    db.execute("INSERT INTO notes (name, text, time) VALUES (?, ?, ?)",#不拼接，留三个槽位，这是模板，焊死形状
               (note["name"], note["text"], note["time"]))#这和上面是同一句话，括号没合上，模板和数据一起交，然后先焊死模板，再灌数据，按位置一一对应灌进三个槽位
    db.commit()#提交
    db.close() #跟57一样
    return jsonify({"ok":True}) 





# 启动服务器，监听 5000 端口（可以理解为：在 5000 号窗口办公）
app.run(debug=True, port=5000)
