# -*- coding: utf-8 -*-

from yunbk import YunBK
from yunbk.backend.local import LocalBackend

import sh

backend = LocalBackend('/data/release/backup')

with YunBK('mysql', backend) as ybk:
    sh.mysqldump(u='root',
                 all_databases=True,
                 _out="dump.sql")
    ybk.backup()
