# 通过这个类，可以向fdfs服务器上传文件
from fdfs_client.client import Fdfs_client
# 根据配置文件创建客户端对象
# 在配置文件中指定了tracker服务器
client = Fdfs_client('/etc/fdfs/client.conf')
# 上传文件
result = client.upload_by_file('*.jpg')
print(result)