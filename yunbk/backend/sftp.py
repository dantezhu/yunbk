# -*- coding: utf-8 -*-

import os
import errno
import paramiko
from .base import BaseBackend
from ..utils import filter_delete_filename_list


class SFTPBackend(BaseBackend):
    """
    ssh后端
    """

    host = None
    port = None
    username = None
    password = None
    remote_dir = None
    sftp = None

    def __init__(self, host, username, password, remote_dir, port=None):
        super(SFTPBackend, self).__init__()
        self.host = host
        self.port = port or 22
        self.username = username
        self.password = password
        self.remote_dir = remote_dir

        # 初始化
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(transport)

    def upload(self, file_path, category):
        """
        上传
        """
        filename = os.path.basename(file_path)

        dst_dir = os.path.join(self.remote_dir, category)
        try:
            self.sftp.stat(dst_dir)
        except IOError, e:
            # 说明没有文件
            if e.errno == errno.ENOENT:
                self.sftp.mkdir(dst_dir)
            else:
                raise e

        remote_path = os.path.join(dst_dir, filename)
        self.sftp.put(file_path, remote_path)

    def clean(self, category, keeps):
        dst_dir = os.path.join(self.remote_dir, category)

        delete_filename_list = filter_delete_filename_list(self.sftp.listdir(dst_dir), keeps)
        for filename in delete_filename_list:
            self.sftp.remove(os.path.join(dst_dir, filename))
