# -*- coding: utf-8 -*-

import os
from .base import BaseBackend
import shutil
from ..utils import filter_delete_filename_list


class LocalBackend(BaseBackend):
    """
    本地后端
    """

    remote_dir = None

    def __init__(self, remote_dir):
        super(LocalBackend, self).__init__()
        self.remote_dir = remote_dir

    def upload(self, file_path, category):
        """
        上传
        """

        dst_dir = os.path.join(self.remote_dir, category)

        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

        if os.path.isfile(dst_dir):
            raise ValueError('dst_dir should be dir. %s' % dst_dir)

        shutil.copy(file_path, dst_dir)

    def clean(self, category, keeps):
        """
        删除掉不需要的
        """
        dst_dir = os.path.join(self.remote_dir, category)

        delete_filename_list = filter_delete_filename_list(os.listdir(dst_dir), keeps)
        for filename in delete_filename_list:
            os.remove(os.path.join(dst_dir, filename))
