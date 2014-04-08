# -*- coding: utf-8 -*-

import os
import datetime
import tarfile


class YunBK(object):

    def backup(self, path, backend):
        """
        备份对应的path
        """
        now = datetime.datetime.now()
        str_now = now.strftime('%Y%m%d_%H%M%S')

        if not os.path.exists(path):
            return -1

        tar_prefix = os.path.basename(os.path.dirname(os.path.join(path, '')))

        tar_filepath = '/tmp/%s.%s.tar' % (tar_prefix, str_now)

        with tarfile.open(tar_filepath, "w") as tar:
            tar.add(path)

        backend.upload(tar_filepath)

        os.remove(tar_filepath)
