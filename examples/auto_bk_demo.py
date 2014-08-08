# -*- coding: utf-8 -*-

import datetime
import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED
from yunbk.yunbk import YunBK
from yunbk.backend.local import LocalBackend


logger = logging.getLogger('main')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

# daemon = True 代表子线程会随主线程一起结束
sched = BackgroundScheduler(daemon=True)


def error_listener(event):
    if event.exception:
        logger.fatal('job %s error. scheduled_run_time: %s, exception: %s, traceback:\n %s',
                     event.job_id, event.scheduled_run_time, event.exception, event.traceback)
    else:
        logger.info('job %s miss', event.job_id)


@sched.scheduled_job('cron', day_of_week='0-5', hour='9-12,13-24', second='*')
def job():
    logger.debug(datetime.datetime.now())
    backend = LocalBackend('/data/release/backup/')
    with YunBK('ybk', [backend]) as ybk:
        f = open('t2.txt', 'w')
        f.write('ok')
        f.close()
        ybk.backup()


def main():
    sched.add_listener(error_listener, EVENT_JOB_ERROR | EVENT_JOB_MISSED)
    sched.start()

    while 1:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
        except:
            logger.error('exc occur.', exc_info=True)
            break


if __name__ == '__main__':
    main()

