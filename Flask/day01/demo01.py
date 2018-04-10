from flask import Flask
from flask import abort

app = Flask(__name__)

""" 传递参数， int类型，float类型，path，不写默认是string类型"""
@app.route('/<int:id>')
def hello_world(id):
    print app.url_map

    """使用abort抛出一个http标准中不存在的自定义的状态码"""
    # abort(404)
    """在响应后添加状态码， 在后一个参数是设置响应行"""
    return "hello world %d" % id, 200, "Connection: keep-alive"


if __name__ == '__main__':
    app.run(debug=True)
