# -*- coding: utf-8 -*-

import datetime
from apscheduler.scheduler import Scheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED
import logging

from yunbk.yunbk import YunBK
from yunbk.backend.local import LocalBackend


logger = logging.getLogger('default')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

sched = Scheduler(daemonic=False)
ybk = YunBK()
bk_backend = LocalBackend('/data/release/backup/')


def err_listener(ev):
    if ev.exception:
        logger.fatal('%s error.', str(ev.job), exc_info=True)
    else:
        logger.info('%s miss', str(ev.job))


@sched.cron_schedule(second='1')
def job():
    logger.debug(datetime.datetime.now())
    ybk.backup(bk_backend, '/Users/zny2008/gitdata/yunbk')
    pass


if __name__ == '__main__':
    sched.add_listener(err_listener, EVENT_JOB_ERROR | EVENT_JOB_MISSED)
    sched.start()

