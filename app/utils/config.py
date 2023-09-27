# -*- encoding: utf-8 -*-
'''
@File    :   config.py
@Time    :   2023/09/25 11:09:06
@Author  :   Zhangziheng
'''

## Flask Config File
import os

PORT = 24001
HOST = "0.0.0.0"
DEBUG = False

## DATABASE
DB = "sqlite" # mysql or sqlite

## MYSQL
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASS = "123"
MYSQL_DB = "DashBoard"

## SQLLite
DB_FILE  = "DashBoard.db"

if DB == "mysql":
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
else:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_FILE}'

# flask_SCHEDULER 的配置
SCHEDULER_API_ENABLED = True
SCHEDULER_TIMEZONE = 'Asia/Shanghai'

# flask_sqlalchemy 的配置
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_POOL_PRE_PING = True
SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle': 280, 'pool_pre_ping': True}


## UNRAID CONFIG
## !!warning!! 无论任何时候 都不要将用户名和密码发布到任何公众网络上！！！
## !!warning!! Please never disclose your username and password on any public network, regardless of the circumstances!

UNRAID_HOST_TYPE =os.getenv("UNRAID_HOST_TYPE", 0)
UNRAID_HOST = os.getenv("UNRAID_HOST", "192.168.0.1")
UNRAID_USERNAME = os.getenv("UNRAID_USERNAME", "root")
UNRAID_PASSWORD = os.getenv("UNRAID_PASSWORD", "123456")



