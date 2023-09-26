# -*- encoding: utf-8 -*-
'''
@File    :   model.py
@Time    :   2023/09/25 11:21:58
@Author  :   Zhangziheng 
'''

from app.ext import db


class CpuStatus(db.Model):
    __tablename__ = "cpu_Status"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   comment="主键")
    cpuLoad = db.Column(db.Integer, comment="cpu总负载")
    otherCpuLoad = db.Column(db.String(255), comment="其他cpu负载")
    uploadTime = db.Column(db.DateTime, comment="上传时间")

    def to_dict(self):
        return {
            "id": self.id,
            "cpuLoad": self.cpuLoad,
            "otherCpuLoad": self.otherCpuLoad,
            "uploadTime": self.uploadTime
        }


class DiskStatus(db.Model):
    __tablename__ = "disk_Status"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   comment="主键")
    diskname = db.Column(db.String(255), comment="磁盘名称")
    diskload = db.Column(db.String(255), comment="磁盘负载")
    diskstatus = db.Column(db.String(255), comment="磁盘状态")
    uploadTime = db.Column(db.DateTime, comment="上传时间")

    def to_dict(self):
        return {
            "id": self.id,
            "diskname": self.diskname,
            "diskload": self.diskload,
            "diskstatus": self.diskstatus,
            "uploadTime": self.uploadTime
        }


class RamStatus(db.Model):
    __tablename__ = "ram_Status"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   comment="主键")
    ramStuats = db.Column(db.String(255), comment="内存状态")
    uploadTime = db.Column(db.DateTime, comment="上传时间")

    def to_dict(self):
        return {
            "id": self.id,
            "ramStuats": self.ramStuats,
            "uploadTime": self.uploadTime
        }


class SpeedStatus(db.Model):
    __tablename__ = "speed_Status"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   comment="主键")
    up = db.Column(db.Float, comment="上传速度 Mbps")
    down = db.Column(db.Float, comment="下载速度 Mbps")
    uploadTime = db.Column(db.DateTime, comment="上传时间")

    def to_dict(self):
        return {
            "id": self.id,
            "up": round(self.up,2),
            "down": round(self.down,2),
            "uploadTime": self.uploadTime
        }


class UpsStatus(db.Model):
    __tablename__ = "ups_Status"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   comment="主键")
    ups_type = db.Column(db.String(255), comment="UPS型号")
    ups_status = db.Column(db.String(255), comment="UPS状态")
    ups_power = db.Column(db.String(255), comment="UPS当前剩余电量")
    ups_now = db.Column(db.String(255), comment="UPS当前负载")
    uploadTime = db.Column(db.DateTime, comment="上传时间")
    
    def to_dict(self):
        return {
            "id": self.id,
            "ups_type": self.ups_type,
            "ups_status": self.ups_status,
            "ups_power": self.ups_power,
            "ups_now": self.ups_now,
            "uploadTime": self.uploadTime
        }
    

class AppAddr(db.Model):
    __tablename__ = "app_addr"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   comment="主键")
    app_name = db.Column(db.String(255), comment="应用名称")
    app_addr = db.Column(db.String(255), comment="应用地址")
    
    def to_dict(self):
        return {
            "id": self.id,
            "app_name": self.app_name,
            "app_addr": self.app_addr
        }