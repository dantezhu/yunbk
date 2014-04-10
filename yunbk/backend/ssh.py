# -*- coding: utf-8 -*-

import os
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

        remote_path = os.path.join(self.remote_dir, category, filename)

        sftp.put(file_path, remote_path)
