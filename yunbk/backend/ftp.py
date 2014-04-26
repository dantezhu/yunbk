# -*- coding: utf-8 -*-

import os
from ftplib import FTP
from .base import BaseBackend


class FTPBackend(BaseBackend):
    """
    ssh后端
    """

    host = None
    port = None
    username = None
    password = None
    remote_dir = None

    def __init__(self, host, username, password, remote_dir, port=None):
        super(FTPBackend, self).__init__()
        self.host = host
        self.port = port or 21
        self.username = username
        self.password = password
        self.remote_dir = remote_dir

    def upload(self, file_path, category):
        """
        上传
        """
        filename = os.path.basename(file_path)

        dst_dir = os.path.join(self.remote_dir, category)
        remote_path = os.path.join(dst_dir, filename)

        client = FTP()
        client.connect(self.host, self.port)
        client.login(self.username, self.password)

        try:
            client.cwd(dst_dir)
        except:
            client.mkd(dst_dir)

        with open(file_path, 'rb') as local_file:
            client.storbinary('STOR ' + remote_path, local_file)

        client.quit()
