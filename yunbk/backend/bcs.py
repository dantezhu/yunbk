# -*- coding: utf-8 -*-

import os
from .base import BaseBackend
from pybcs import BCS

BCS_HOST = 'bcs.duapp.com'


class BCSBackend(BaseBackend):
    """
    本地后端
    """

    bcs = None
    bucket = None

    def __init__(self, ak, sk, bucket_name, host=None):
        super(BCSBackend, self).__init__()
        self.bcs = BCS(host or BCS_HOST, ak, sk)
        self.bucket = self.bcs.bucket(bucket_name)

    def upload(self, file_path):
        """
        上传
        """

        filename = os.path.basename(file_path)

        self.bucket.create()
        obj = self.bucket.object(filename)

        with open(file_path, 'rb') as f:
            obj.put_file(f)
