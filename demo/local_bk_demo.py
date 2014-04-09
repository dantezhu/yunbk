# -*- coding: utf-8 -*-

from yunbk import YunBK
from yunbk.backend.local import LocalBackend

bk = YunBK()

backend = LocalBackend('/data/release/backup')

bk.backup(backend, '/Users/zny2008/gitdata/yunbk')
