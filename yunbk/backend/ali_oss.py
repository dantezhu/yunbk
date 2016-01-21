# -*- coding: utf-8 -*-
"""
阿里云 OSS SDK: https://docs.aliyun.com
"""

import os
import oss2
from .base import BaseBackend
from ..utils import filter_delete_filename_list


class OSSBackend(BaseBackend):
    """
    阿里OSS后端
    """

    bucket = None

    def __init__(self, access_key_id, access_key_secret, host, bucket_name):
        """
        access_key_id:
        access_key_secret:
        host: 域名，如 http://oss-cn-hangzhou.aliyuncs.com
        bucket_name: 需要提前在后台创建好，这里不再自动创建
        """
        super(OSSBackend, self).__init__()
        auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(auth, host, bucket_name)

    def upload(self, file_path, category):
        """
        上传
        """

        filename = os.path.basename(file_path)

        rsp = self.bucket.put_object_from_file(
            os.path.join(category, filename),
            file_path,
        )

        if rsp.status != 200:
            raise Exception('put_object_from_file fail: <%s> %s' % (rsp.status, rsp.read()))

    def clean(self, category, keeps):
        object_list = self.bucket.list_objects(category+'/')

        delete_filename_list = filter_delete_filename_list(object_list, keeps)
        self.bucket.batch_delete_objects(delete_filename_list)
