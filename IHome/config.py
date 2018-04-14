#!/usr/bin/ python3
# -*-coding:utf-8-*-

# 先在当前类中定义配置的类，并从中加载配置
import redis


# 配置app的配置类
class BaseConfig:

    SECRET_KEY = "laizonghuiyilu"


    # 导入数据库扩展，并在配置中填写相关配置
    # mysql 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@localhost:3306/ihome_flask"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 创建redis存储对象，并在配置中填写相关配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # 利用flask - session扩展，将session数据保存到Redis中
    # flask_session的配置信息
    SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
    SESSION_USE_SIGNER = True  # 让 cookie 中的 session_id 被加密签名处理
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 使用 redis 的实例
    PERMANENT_SESSION_LIFETIME = 86400  # session 的有效期，单位是秒

class DevelopementConfig(BaseConfig):
    """开发模式下的配置"""
    DEBUG = True


class ProductionConfig(BaseConfig):
    """生产模式下的配置"""
    pass


# 定义配置字典字典
config = {
    "development": DevelopementConfig,
    "production": ProductionConfig
}