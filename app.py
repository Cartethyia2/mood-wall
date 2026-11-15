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


# ================= 心情墙的"仓库" =================
# 先放一个 Python 列表当临时仓库，里面已经贴了两张示例纸条
# （注意：它住在内存里，服务器一关就全没了——下节课换数据库解决）
NOTES = [
    {"name": "小K", "text": "今天广州下雨，适合摸头", "time": "2026-11-14 18:00"},
    {"name": "刳云", "text": "后端课第一天，我居然在写服务器", "time": "2026-11-14 18:01"},
]

@app.route("/api/notes")#以后敲这个地址的，GET这个门被敲，找下面的函数
def send_notes(): #定义一个能发送小纸条的函数
    return jsonify(NOTES) #打包寄给浏览器


@app.route("/api/notes",methods =["POST"]) #POST这个门被敲，找下面的函数
def receive_notes(): #定义包裹接收的函数
    note=request.get_json() #拆包裹里面的小纸条
    note["time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    NOTES.append(note) #这个是把什么东西搞到服务器内存里面，用append搞进去
    return jsonify({"ok":True}) #回执，类似“已签收”





# 启动服务器，监听 5000 端口（可以理解为：在 5000 号窗口办公）
app.run(debug=True, port=5000)
