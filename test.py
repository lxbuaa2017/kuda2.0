import json
from flask import Flask
from flask import request
import json
import requests

app = Flask(__name__)

# 4.提供rest服务
# 用户提交post请求，body是{"text":""}
@app.route('/', methods=["POST"])
def rest():
    res = request.data.decode('UTF-8').replace("'",'"')
    spo_obj = json.loads(res)
    spo_list = spo_obj['spos']
    global segmentor
    global postagger

    return ""


if __name__ == '__main__':
    global segmentor
    global postagger

    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0", port=5000, debug=True)
