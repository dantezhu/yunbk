# -*- coding: utf-8 -*-

import os
from baidupcs import PCS, tools

from .base import BaseBackend


class BaiDuYunBackend(BaseBackend):

    pcs = None
    refresh_token = None
    remote_dir = None
    client_id = None
    client_secret = None

    def __init__(self, access_token, remote_dir=None,
                 refresh_token=None,
                 client_id=None,
                 client_secret=None
        ):
        """
        access_token: 访问数据token。有效期1个月
        remote_dir: 对端要存放的目录地址
        refresh_token: refresh_token。有效期10年
        client_id: 更新access_token需要
        client_secret: 更新access_token需要
        """
        super(BaiDuYunBackend, self).__init__()

        self.pcs = PCS(access_token)
        self.remote_dir = remote_dir or '/apps/'
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.client_secret = client_secret

    def refresh_access_token(self):
        """
        获取新的refresh token
        """
        rsp = tools.get_new_access_token(self.refresh_token, self.client_id, self.client_secret)

        access_token = rsp.json().get('access_token')
        self.pcs = PCS(access_token)

    def upload(self, file_path):
        """
        上传
        """
        filename = os.path.basename(file_path)
        remote_path = os.path.join(self.remote_dir, filename)

        local_file = open(file_path, 'rb')

        rsp = self.pcs.upload(remote_path, local_file)
        if rsp.status_code == 401 and rsp.json().get('error_code') in (110, 111):
            self.refresh_access_token()
            rsp = self.pcs.upload(remote_path, local_file)

        local_file.close()

        return rsp
