# -*- encoding: utf-8 -*-
'''
@File    :   webData.py
@Time    :   2023/09/26 09:56:08
@Author  :   Zhangziheng 
'''

import datetime

from flask import Blueprint, current_app, jsonify, request

from ..utils.model import *

api_blueprint = Blueprint('webData', __name__, url_prefix='/web')


@api_blueprint.route("/getData", methods=['POST'])
def getData():
    """根据传输过来
    {
        "find" : 1
    }
    Returns:
        _type_: _description_
    """
    requetsJson = request.json
    if not requetsJson:
        return jsonify({"code": 200, "data": {}, "msg": "no data"})
    # -- find : 以天为单位查找
    findTime = requetsJson.get("find", None)
    findType = requetsJson.get("type", None)
    if not findTime or not findType:
        return jsonify({"code": 200, "data": {}, "msg": "no data"})
    # 按照findTime的类型 筛选库中的数据 并且展示
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=findTime)
    if findType == 1:
        raw_result_dict = RamStatus.query.filter(
            RamStatus.uploadTime.between(start_date, end_date)).order_by(
                RamStatus.uploadTime.desc()).first()
        cpu_result_dict = raw_result_dict.to_dict()
        raw_result_list = [cpu_result_dict]

        cpu_result_dict = CpuStatus.query.filter(
            CpuStatus.uploadTime.between(start_date, end_date)).order_by(
                CpuStatus.uploadTime.desc()).first()
        cpu_result_dict = cpu_result_dict.to_dict()
        cpu_result_list = [cpu_result_dict]

        speed_result_dict = SpeedStatus.query.filter(
            SpeedStatus.uploadTime.between(start_date, end_date)).order_by(
                SpeedStatus.uploadTime.desc()).first()
        speed_result_dict = speed_result_dict.to_dict()
        speed_result_list = [speed_result_dict]

        disk_result_dict = DiskStatus.query.filter(
            DiskStatus.uploadTime.between(start_date, end_date)).order_by(
                DiskStatus.uploadTime.desc()).first()
        disk_result_dict = disk_result_dict.to_dict()
        disk_result_list = [disk_result_dict]
    else:
        raw_result_dict = RamStatus.query.filter(
            RamStatus.uploadTime.between(start_date, end_date)).all()
        raw_result_list = [i.to_dict() for i in raw_result_dict]

        cpu_result_dict = CpuStatus.query.filter(
            CpuStatus.uploadTime.between(start_date, end_date)).all()
        cpu_result_list = [i.to_dict() for i in cpu_result_dict]

        speed_result_dict = SpeedStatus.query.filter(
            SpeedStatus.uploadTime.between(start_date, end_date)).all()
        speed_result_list = [i.to_dict() for i in speed_result_dict]

        disk_result_dict = DiskStatus.query.filter(
            DiskStatus.uploadTime.between(start_date, end_date)).all()
        disk_result_list = [i.to_dict() for i in disk_result_dict]
    return jsonify({
        "code": 200,
        "data": {
            "raw": raw_result_list,
            "cpu": cpu_result_list,
            "speed": speed_result_list,
            "disk": disk_result_list
        },
        "msg": "success"
    })
