# -*- coding: utf-8 -*-


class BaseBackend(object):

    def upload(self, file_path, folder):
        raise NotImplementedError('not implemented')