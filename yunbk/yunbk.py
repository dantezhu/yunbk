# -*- coding: utf-8 -*-

import os
import datetime
import tarfile
import tempfile
import logging
import shutil

import sh

import constants

logger = logging.getLogger(__name__)


class YunBK(object):

    def __init__(self, backup_name, backends, keeps=None):
        self.backup_name = backup_name
        self.backends = backends
        self.keeps = keeps
        self.dir_prefix = "{0}_".format(backup_name)

    def __enter__(self):
        """Save the old current working directory,
            create a temporary directory,
            and make it the new current working directory.
        """
        self.old_cwd = os.getcwd()
        self.tmpd = tempfile.mkdtemp(prefix=self.dir_prefix)
        sh.cd(self.tmpd)
        logger.info("New current working directory: %s.", self.tmpd)
        return self

    def __exit__(self, type, value, traceback):
        """Reseting the current working directory,
            and run synchronization if enabled.
        """
        sh.cd(self.old_cwd)
        logger.info("Back to %s", self.old_cwd)
        shutil.rmtree(self.tmpd)

    def backup(self):
        """
        备份对应的path
        """

        now = datetime.datetime.now()
        str_now = now.strftime(constants.STRFTIME_TPL)

        tar_filepath = os.path.join(tempfile.gettempdir(), '%s.%s.tar' % (self.backup_name, str_now))

        logger.info('tar_filepath: %s', tar_filepath)

        with tarfile.open(tar_filepath, "w") as tar:
            tar.add(self.tmpd, os.path.basename(self.tmpd))

        try:
            for backend in self.backends:
                backend.upload(tar_filepath, self.backup_name)
        except Exception, e:
            raise e
        finally:
            os.remove(tar_filepath)

        # 清理
        self.rotate()

    def rotate(self):
        """
        清理无用的
        """
        if not self.keeps:
            # 就是不删除
            return

        for backend in self.backends:
            backend.clean(self.backup_name, self.keeps)
