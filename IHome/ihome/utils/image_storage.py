#!/usr/bin/ python3
# -*-coding:utf-8-*-

from qiniu import Auth, put_file, put_data


def image_storage(image_data):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'v3n5FPnRvLujRroKe3X9FxjMSgtWCmMWBeharusu'
    secret_key = 'd3uJUlaQ9iKh0b5XkhU-Tlx5hjrDiWDDeHA4xotw'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'ihome5'

    # 上传到七牛后保存的文件名
    # 如果不指定七牛会帮我自动维护图片的名字
    # key = 'my-python-logo.png';

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name)

    # 要上传文件的本地路径

    # localfile = './77.png'
    # ret, info = put_file(token, None, "./avop00127pl.jpg")
    ret, info = put_data(token, None, image_data)


    # print info
    # print ret

    # 上传成功直接返回图片名, 失败则报异常
    if info.status_code == 200:
        return ret["key"]
    else:
        raise Exception("上传图像失败")


if __name__ == '__main__':
    with open("./avop00127pl.jpg") as file:
        image_storage(file.read())
