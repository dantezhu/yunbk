# -*- coding: utf-8 -*-

import datetime
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED
from yunbk.yunbk import YunBK
from yunbk.backend.local import LocalBackend


logger = logging.getLogger('main')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

sched = BlockingScheduler()


def error_listener(event):
    if event.exception:
        logger.fatal('job %s error. scheduled_run_time: %s, exception: %s, traceback:\n%s',
                     event.job_id, event.scheduled_run_time, event.exception, event.traceback)
    else:
        logger.info('job %s miss', event.job_id)


@sched.scheduled_job('cron', day_of_week='0-5', hour='9-12,13-24', second='*')
def backup():
    logger.debug(datetime.datetime.now())
    backend = LocalBackend('/data/release/backup/')
    with YunBK('ybk', [backend]) as ybk:
        with open('t.txt', 'w') as f:
            f.write('ok')

        ybk.backup()


def main():
    sched.add_listener(error_listener, EVENT_JOB_ERROR | EVENT_JOB_MISSED)

    try:
        sched.start()
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    main()

