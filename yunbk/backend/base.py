# -*- coding: utf-8 -*-


class BaseBackend(object):

    def upload(self, filename):
        raise NotImplementedError('not implemented')