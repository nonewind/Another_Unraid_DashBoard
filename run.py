# -*- encoding: utf-8 -*-
'''
@File    :   run.py
@Time    :   2023/09/25 10:06:18
@Author  :   Zhangziheng
'''

from concurrent.futures import ThreadPoolExecutor

from app import create_app, logger, scheduler
from app.tasks.backTask import getCpuload, getUPSload

logger.info("DashBoard Start Init...")

app = create_app()
scheduler.start()
apithead = ThreadPoolExecutor(max_workers=2)
try:
    # 注册启动两个后台任务
    logger.warning("start run task")
    apithead.submit(getCpuload)
    apithead.submit(getUPSload)
    # apithead.submit(logTask)
    logger.info("success to start apithead")
except:
    logger.error("fail to start apithead")

if __name__ == "__main__":
    app.run(host=app.config["HOST"],
            port=app.config["PORT"],
            debug=app.config["DEBUG"])
