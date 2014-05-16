# -*- coding: utf-8 -*-
"""
BCS SDK: http://developer.baidu.com/wiki/index.php?title=docs/cplat/bcs/sdk
"""

import os
from .base import BaseBackend
from pybcs import BCS
from ..utils import filter_delete_filename_list

BCS_HOST = 'bcs.duapp.com'


class BCSBackend(BaseBackend):
    """
    百度BCS后端
    """

    bucket_name = None
    bcs = None
    bucket = None

    def __init__(self, ak, sk, bucket_name, host=None):
        super(BCSBackend, self).__init__()
        self.bucket_name = bucket_name
        self.bcs = BCS(host or BCS_HOST, ak, sk)
        self.bucket = self.bcs.bucket(bucket_name)

    def upload(self, file_path, category):
        """
        上传
        """

        filename = os.path.basename(file_path)

        if self.bucket_name not in [bucket.bucket_name for bucket in self.bcs.list_buckets()]:
            self.bucket.create()

        obj = self.bucket.object(os.path.join('/', category, filename))
        obj.put_file(file_path)

    def clean(self, category, keeps):
        # 和阿里云不一样，必须以 / 开头
        obj_list = self.bucket.list_objects('/' + category + '/')
        filename_list = [obj.object_name for obj in obj_list]

        delete_filename_list = set(filter_delete_filename_list(filename_list, keeps))
        for obj in obj_list:
            if obj.object_name in delete_filename_list:
                obj.delete()
