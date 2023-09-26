# -*- encoding: utf-8 -*-
'''
@File    :   error.py
@Time    :   2023/09/26 09:39:42
@Author  :   Zhangziheng 
'''


from flask import Blueprint, render_template, current_app

api_blueprint = Blueprint('error', __name__, url_prefix='/')

@api_b