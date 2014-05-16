# -*- coding: utf-8 -*-

from yunbk import YunBK
from yunbk.backend.local import LocalBackend
from yunbk.constants import KEEPS_NORMAL

import logging
logger = logging.getLogger('yunbk')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

backend = LocalBackend('/data/backup')
with YunBK('yb', [backend], keeps=KEEPS_NORMAL) as ybk:
    f = open('t.txt', 'w')
    f.write('ok')
    f.close()
    ybk.backup()
