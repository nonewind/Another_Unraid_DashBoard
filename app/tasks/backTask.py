# -*- encoding: utf-8 -*-
'''
@File    :   backTask.py
@Time    :   2023/09/25 11:16:36
@Author  :   Zhangziheng 
'''

import datetime
import re

from app import app, db, scheduler

import websocket
from ..ext import G_logger as logger
from ..ext import queue
from ..unraid.unraid import UnraidApi
from ..utils.model import (CpuStatus, DiskStatus, RamStatus, SpeedStatus,
                           UpsStatus)

logger.info("BackTask Start Running...")


@scheduler.task("interval", id="job_0_delData", minutes=30)
def job_0_delData():
    """
    查找当前数据库中的数据 如果超过1小时就删除
    """
    logger.info("start job_0_delData")
    _now = datetime.datetime.now()
    _delTime_str = (_now -
                    datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    # _delTime_str = (_now - datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")
    sql_del_cpu = f"delete from {CpuStatus.__tablename__} where uploadTime < '{_delTime_str}'"
    sql_del_disk = f"delete from {DiskStatus.__tablename__} where uploadTime < '{_delTime_str}'"
    sql_del_ram = f"delete from {RamStatus.__tablename__} where uploadTime < '{_delTime_str}'"
    sql_del_speed = f"delete from {SpeedStatus.__tablename__} where uploadTime < '{_delTime_str}'"
    # 执行sql
    with app.app_context():
        db.session.execute(sql_del_cpu)
        db.session.commit()
        db.session.execute(sql_del_disk)
        db.session.commit()
        db.session.execute(sql_del_ram)
        db.session.commit()
        db.session.execute(sql_del_speed)
        db.session.commit()

    logger.info("success to delData")


def getUPSload():
    """
    获取WS中数据 这个请求包含 ups的情况
    """
    logger.info("start getUPSload backT.ask")
    # api = app.config['UNRAID_API']
    api = UnraidApi(username=app.config['UNRAID_USERNAME'],
                    password=app.config['UNRAID_PASSWORD'],
                    baseUrl=app.config['UNRAID_HOST'])
    api._login(type=app.config['UNRAID_HOST_TYPE'])
    ws = api.upsLoad(type=app.config['UNRAID_HOST_TYPE'])
    while True:
        try:
            data = ws.recv_frame().data.decode('utf-8')
        except Exception as e:
            ws = getNewWSconnectin(websocket=ws)
        data = ws.recv_frame().data.decode('utf-8')
        logger.debug(f"getUPSload: {data}")
        # 处理数据 磁盘情况
        data_replace = data.replace("<span>", "<span class='green-text'>")
        _splitData = data_replace.split(";<span class='green-text'>")
        _allList = [_.replace("</span>", "") for _ in _splitData]
        # '47 W (12 %)'
        try:
            newUpsStatus = UpsStatus(
                ups_type=_allList[0],
                ups_status=_allList[1],
                ups_power=_allList[4],
                ups_now=_allList[5].split("(")[-1].replace(" %)", ""),
                uploadTime=datetime.datetime.now())
        except Exception as e:
            logger.error(f"fail to split data: {e}")
            continue

        with app.app_context():
            try:
                db.session.add(newUpsStatus)
                db.session.commit()
            except Exception as e:
                logger.error(f"fail to commit to db: {e}")
                db.session.rollback()


def getCpuload():
    """
    获取WS中数据 这个请求包含 cpu负载 磁盘情况 内存情况 网络情况
    """
    try:
        logger.info("start getCpuload backT.ask")
        api = UnraidApi(username=app.config['UNRAID_USERNAME'],
                        password=app.config['UNRAID_PASSWORD'],
                        baseUrl=app.config['UNRAID_HOST'])
        api._login(type=app.config['UNRAID_HOST_TYPE'])
        ws = api.cpuLoad(type=app.config['UNRAID_HOST_TYPE'])
        while True:
            try:
                data = ws.recv_frame().data.decode('utf-8')
            except Exception as e:
                ws = getNewWSconnectin(websocket=ws)
            logger.debug(f"getCpuload: {data}")
            # 处理数据 磁盘情况
            if "class=" in data:
                _bat_settings = r"settings\">([\S\s]+?)</a>"
                _bat_load = r"class='load'>([\S\s]+?)</span>"
                _bat_status = r"id='text-[\S]+?'>([\S\s]+?)</span>"
                re_settings = re.findall(_bat_settings, data)
                str_settings = ','.join(re_settings)
                re_load = re.findall(_bat_load, data)
                str_load = ','.join(re_load)
                re_status = re.findall(_bat_status, data)
                str_status = ','.join(re_status)

                newDiskStatus = DiskStatus(diskname=str_settings,
                                           diskload=str_load,
                                           diskstatus=str_status,
                                           uploadTime=datetime.datetime.now())

                # 存入数据库
                with app.app_context():
                    try:
                        db.session.add(newDiskStatus)
                        db.session.commit()
                    except Exception as e:
                        logger.error(f"fail to commit to db: {e}")
                        db.session.rollback()
            elif "%" in data:
                # 处理数据 RAM情况
                splitData = data.split("%")[0]
                newRamStatus = RamStatus(ramStuats=splitData,
                                         uploadTime=datetime.datetime.now())
                # 存入数据库
                with app.app_context():
                    try:
                        db.session.add(newRamStatus)
                        db.session.commit()
                    except Exception as e:
                        logger.error(f"fail to commit to db: {e}")
                        db.session.rollback()
            elif 'cpu' in data:
                # 处理数据 CPU情况
                spiltData = data.split("\n")
                allCPUload = [
                    spiltData[spiltData.index(_) + 1].split("=")[1]
                    for _ in spiltData if 'cpu' in _
                ]
                _mainCpuLoad = allCPUload[0]
                del allCPUload[0]
                _otherCpuLoad = ','.join(allCPUload)
                # 存入数据库
                newCpuStatus = CpuStatus(cpuLoad=_mainCpuLoad,
                                         otherCpuLoad=_otherCpuLoad,
                                         uploadTime=datetime.datetime.now())
                with app.app_context():
                    try:
                        db.session.add(newCpuStatus)
                        db.session.commit()
                    except Exception as e:
                        logger.error(f"fail to commit to db: {e}")
                        db.session.rollback()
            elif "bond0" in data:
                # 处理数据 网络情况
                # print(data)

                _bat_bond0 = r"bond0([\d]+?\.[\d]+?) ([K|M|G]?bps)([\d]+?\.[\d]+?) ([K|M|G]?bps)"
                re_bond0 = re.findall(_bat_bond0, data.replace("\x00", ""))
                if not re_bond0:
                    logger.warning(f"unknow data: {data}")
                    up = 0.0
                    down = 0.0
                    # continue
                else:
                    if re_bond0[0][1] == 'Kbps':
                        up = float(re_bond0[0][0]) / 1024
                        down = float(re_bond0[0][2]) / 1024
                    elif re_bond0[0][1] == 'Gbps':
                        up = float(re_bond0[0][0]) * 1024
                        down = float(re_bond0[0][2]) * 1024
                    else:
                        up = float(re_bond0[0][0])
                        down = float(re_bond0[0][2])
                newSpeedStatus = SpeedStatus(
                    up=up, down=down, uploadTime=datetime.datetime.now())
                with app.app_context():
                    try:
                        db.session.add(newSpeedStatus)
                        db.session.commit()
                    except Exception as e:
                        logger.error(f"fail to commit to db: {e}")
                        db.session.rollback()
            else:
                logger.warning(f"unknow data: {data}")
    except Exception as e:
        logger.error(e)


def getNewWSconnectin(
        websocket: websocket.WebSocketApp) -> websocket.WebSocketApp:
    logger.warning("reset the ws connection")
    websocket.close()
    api = UnraidApi(username=app.config['UNRAID_USERNAME'],
                    password=app.config['UNRAID_PASSWORD'],
                    baseUrl=app.config['UNRAID_HOST'])
    api._login(type=app.config['UNRAID_HOST_TYPE'])
    ws = api.cpuLoad(type=app.config['UNRAID_HOST_TYPE'])
    return ws