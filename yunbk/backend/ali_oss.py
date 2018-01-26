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
    阿里OSS后端，依赖 oss v2
    pip install oss2
    """

    bucket = None

    def __init__(self, access_key_id, access_key_secret, host, bucket_name, keeps=None):
        """
        access_key_id:
        access_key_secret:
        host: 域名，如 http://oss-cn-hangzhou.aliyuncs.com
        bucket_name: 不需要在后台自动创建，也会自动创建好
        """
        super(OSSBackend, self).__init__(keeps)
        auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(auth, host, bucket_name)

        service = oss2.Service(auth, host)
        if bucket_name not in [b.name for b in oss2.BucketIterator(service)]:
            # 说明bucket不存在
            self.bucket.create_bucket()

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

    def clean(self, category, keeps=None):
        keeps = keeps or self.keeps
        if not keeps:
            return

        object_list = [obj.key for obj in self.bucket.list_objects(category+'/').object_list]
        delete_filename_list = filter_delete_filename_list(object_list, keeps)
        if delete_filename_list:
            self.bucket.batch_delete_objects(delete_filename_list)
