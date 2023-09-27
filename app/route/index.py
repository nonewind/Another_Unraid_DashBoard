# -*- encoding: utf-8 -*-
'''
@File    :   index.py
@Time    :   2023/09/26 09:36:00
@Author  :   Zhangziheng
'''

from flask import Blueprint, render_template, current_app

api_blueprint = Blueprint('index', __name__, url_prefix='/')


@api_blueprint.route("/")
def index():
    return render_template("/index.html",serverName=current_app.config['SERER_NAME'])