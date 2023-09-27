# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2023/09/25 11:02:15
@Author  :   Zhangziheng 
'''

from flask import Flask, redirect, request
from flask_apscheduler import APScheduler
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile("utils/config.py")

from app.unraid.unraid import UnraidApi

from .ext import G_logger as logger
from .ext import db
from .utils.model import *

scheduler = APScheduler()
db.init_app(app)
migrate = Migrate(app, db)
scheduler.init_app(app)


# 请求路径检查
@app.before_request
def redirect_all_except():
    if (request.path not in ['/', '/index']
            and not request.path.startswith('/web/')
            and not request.path.startswith('/static/')):
        return redirect('/')

def create_app():
    # 设置返回中文
    app.config['JSON_AS_ASCII'] = False
    # logger.info(app.config)
    logger.warning("start init UnraidApi")
    _api = UnraidApi(username=app.config['UNRAID_USERNAME'],
                     password=app.config['UNRAID_PASSWORD'],
                     baseUrl=app.config['UNRAID_HOST'])
    unraidApi = _api._login(type=app.config['UNRAID_HOST_TYPE'])
    if not unraidApi:
        exit("Unraid Login Error")
    logger.warning("init UnraidApi success")
    app.config['SERER_NAME'] = _api.serverName
    # 注册路由
    from .route import index, webData
    app.register_blueprint(index.api_blueprint)
    app.register_blueprint(webData.api_blueprint)
    return app