# -*- coding: utf-8 -*-

import os
from .base import BaseBackend
from pybcs import BCS

BCS_HOST = 'bcs.duapp.com'


class BCSBackend(BaseBackend):
    """
    本地后端
    """

    bucket_name = None
    bcs = None
    bucket = None

    def __init__(self, ak, sk, bucket_name, host=None):
        super(BCSBackend, self).__init__()
        self.bucket_name = bucket_name
        self.bcs = BCS(host or BCS_HOST, ak, sk)
        self.bucket = self.bcs.bucket(bucket_name)

    def upload(self, file_path):
        """
        上传
        """

        filename = os.path.basename(file_path)

        if self.bucket_name not in [bucket.bucket_name for bucket in self.bcs.list_buckets()]:
            self.bucket.create()

        obj = self.bucket.object('/' + filename)
        obj.put_file(file_path)
