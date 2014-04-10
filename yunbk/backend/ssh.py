# -*- coding: utf-8 -*-

import os
import errno
import paramiko
from .base import BaseBackend


class SSHBackend(BaseBackend):
    """
    ssh后端
    """

    host = None
    port = None
    username = None
    password = None
    remote_dir = None

    def __init__(self, host, port, username, password, remote_dir):
        super(SSHBackend, self).__init__()
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.remote_dir = remote_dir

    def upload(self, file_path, category):
        """
        上传
        """
        filename = os.path.basename(file_path)

        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        dst_dir = os.path.join(self.remote_dir, category)
        try:
            sftp.stat(dst_dir)
        except IOError, e:
            # 说明没有文件
            if e.errno == errno.ENOENT:
                sftp.mkdir(dst_dir)
            else:
                raise e

        remote_path = os.path.join(dst_dir, filename)
        sftp.put(file_path, remote_path)
