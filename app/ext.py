# -*- encoding: utf-8 -*-
'''
@File    :   ext.py
@Time    :   2023/09/25 11:05:14
@Author  :   Zhangziheng 
'''


# -- 防止循环引用 --

from flask_sqlalchemy import SQLAlchemy
from .utils.logger import creatLogger
from queue import Queue

db = SQLAlchemy()
queue = Queue()
G_logger = creatLogger("DashBoard")