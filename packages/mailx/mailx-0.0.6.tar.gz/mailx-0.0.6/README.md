# mailx

#### 介绍
快捷使用mail模块

#### 软件架构
软件架构说明


#### 安装教程

1.  pip安装
```shell script
pip install mailx
```
2.  pip安装（使用阿里云镜像加速）
```shell script
pip install mailx -i https://mirrors.aliyun.com/pypi/simple
```


#### 使用说明

1.  demo
```python
import mailx
res = mailx.send_text(sub='test sub', content='test content', to_addrs=['test@test.com'])
```

2. 常用设置
- mail.env：
```text
smtp_host={your smtp_host}
smtp_port={your smtp_port}
from_name={your from_name}
smtp_username={your smtp_username}
smtp_password={your_smtp_username}
to_addrs={your smtp_username, split by ","}
```
- SMTP服务端口号：25或80或465(SSL加密)
