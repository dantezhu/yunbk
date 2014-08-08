# -*- coding: utf-8 -*-

import datetime
from apscheduler2.scheduler import Scheduler
from apscheduler2.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED
import logging

from yunbk.yunbk import YunBK
from yunbk.backend.local import LocalBackend


logger = logging.getLogger('default')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

sched = Scheduler(daemonic=False)


def err_listener(ev):
    if ev.exception:
        logger.fatal('%s error.', str(ev.job), exc_info=True)
    else:
        logger.info('%s miss', str(ev.job))


@sched.cron_schedule(second='1')
def job():
    logger.debug(datetime.datetime.now())
    backend = LocalBackend('/data/release/backup/')
    with YunBK('ybk', [backend]) as ybk:
        f = open('t2.txt', 'w')
        f.write('ok')
        f.close()
        ybk.backup()


if __name__ == '__main__':
    sched.add_listener(err_listener, EVENT_JOB_ERROR | EVENT_JOB_MISSED)
    sched.start()

