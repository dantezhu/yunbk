# -*- coding: utf-8 -*-

import os
from .base import BaseBackend
import shutil


class LocalBackend(BaseBackend):
    """
    本地后端
    """

    host = None
    port = None
    username = None
    password = None
    remote_dir = None

    def __init__(self, remote_dir):
        super(LocalBackend, self).__init__()
        self.remote_dir = remote_dir

    def upload(self, file_path):
        """
        上传
        """
        if not os.path.exists(self.remote_dir):
            os.makedirs(self.remote_dir)

        if os.path.isfile(self.remote_dir):
            raise ValueError('remote_dir should be dir. %s' % self.remote_dir)

        shutil.copyfile(file_path, self.remote_dir)
