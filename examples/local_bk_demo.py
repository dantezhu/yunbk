# -*- coding: utf-8 -*-

from yunbk import YunBK
from yunbk.backend.local import LocalBackend
from yunbk.constants import KEEPS_NORMAL
import sh
import shutil

import logging
logger = logging.getLogger('yunbk')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

backend = LocalBackend('/data/backup')
with YunBK('yb', [backend], keeps=KEEPS_NORMAL) as ybk:
    # 生成文件
    with open('t.txt', 'w') as f:
        f.write('ok')

    # 备份文件
    shutil.copy('/data/store/db.sqlite3', 'db.sqlite3')

    # 备份目录，如redis
    shutil.copytree('/data/store/redis', 'redis')

    # 备份mysql所有库
    sh.mysqldump(
        u='root',
        all_databases=True,
        _out="dump_all.sql"
    )

    # 备份mysql某个库
    sh.mysqldump(
        'db1',
        "--ignore-table=db1.tb1",
        u='root',
        p='passwd',
        _out="dump_db1.sql"
    )

    # 备份mongodb
    sh.mongodump(
        u='root',
        p='passwd',
        h='127.0.0.1',
        port=27017,
        d='db1',  # 不传-d参数即备份所有库
        o='mongo_dump',
    )

    ybk.backup()
