# -*- coding: utf-8 -*-

import os
from ftplib import FTP
from .base import BaseBackend
from ..utils import filter_delete_filename_list


class FTPBackend(BaseBackend):
    """
    ssh后端
    """

    host = None
    port = None
    username = None
    password = None
    remote_dir = None

    ftp = None

    def __init__(self, host, username, password, remote_dir, port=None):
        super(FTPBackend, self).__init__()
        self.host = host
        self.port = port or 21
        self.username = username
        self.password = password
        self.remote_dir = remote_dir

        self.ftp = FTP()
        self.ftp.connect(self.host, self.port)
        self.ftp.login(self.username, self.password)

    def upload(self, file_path, category):
        """
        上传
        """
        filename = os.path.basename(file_path)

        dst_dir = os.path.join(self.remote_dir, category)
        remote_path = os.path.join(dst_dir, filename)

        try:
            self.ftp.cwd(dst_dir)
        except:
            self.ftp.mkd(dst_dir)

        with open(file_path, 'rb') as local_file:
            self.ftp.storbinary('STOR ' + remote_path, local_file)

        #self.ftp.quit()

    def clean(self, category, keeps):
        dst_dir = os.path.join(self.remote_dir, category)
        filename_list = self.ftp.nlst(dst_dir)

        delete_filename_list = filter_delete_filename_list(filename_list, keeps)
        for filename in delete_filename_list:
            self.ftp.delete(os.path.join(dst_dir, filename))
