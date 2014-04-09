# -*- coding: utf-8 -*-

from yunbk import YunBK
from yunbk.backend.local import LocalBackend

import logging
logger = logging.getLogger('yunbk')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

backend = LocalBackend('/data/release/backup')
with YunBK('yb', backend) as ybk:
    f = open('t.txt', 'w')
    f.write('ok')
    f.close()
    ybk.backup()
