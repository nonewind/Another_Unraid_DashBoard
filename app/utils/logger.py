# -*- encoding: utf-8 -*-
'''
@File    :   logger.py
@Time    :   2023/09/25 11:13:54
@Author  :   Zhangziheng 
'''
import logging



def creatLogger(name):
    """创建logger

    Args:
        name (string): 打印者的名称

    Returns:
        logger
    """
    datefmt = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(
        level=logging.INFO,
        datefmt=datefmt,
        format='[%(asctime)s] [%(name)s] [%(levelname)s] :: %(message)s')
    return logging.getLogger(name)