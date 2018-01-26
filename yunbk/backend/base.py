# -*- coding: utf-8 -*-


class BaseBackend(object):

    # 文件保存时间。
    keeps = None

    def __init__(self, keeps=None):
        self.keeps = keeps

    def upload(self, file_path, folder):
        raise NotImplementedError('not implemented')

    def clean(self, category, keeps=None):
        raise NotImplementedError('not implemented')
