from flask import Flask

#2.完成路径
# 静态资源路径,如果不指定static_url_path 默认路径就是/ static ,也可以手动指定
# 静态资源文件夹,如果不指定static_folder 默认路径就是 static ,也可以手动指定
# 模板文件夹,如果不指定template_folder 默认路径就是templates ,也可以手动指定
app = Flask(__name__)

#3.使用应用程序app装饰了视图函数, 将视图函数和路由中的路径绑定在了一起
# 一旦访问路由中的地址, 就会自动执行视图函数
@app.route('/index/user')
def index():

    # raise Exception("big error")
    return "index"

# 当直接从该文件启动程序的时候__name__就是__main__
# 如果从其他文件中调用到当前文件,那么__name__就是demo02
if __name__ == '__main__':
    """ 默认host是: 127.0.0.1  如果设置成0.0.0.0 那么可以通过外部来进行访问. 内部还是通过127.0.0.1访问
    默认的端口是: 5000
    debug参数默认是False
    如果改成True之后可以进行动态部署不需要重新启动程序,并且报错之后有友情提示"""
    app.run(host="0.0.0.0", port=5001, debug=True)