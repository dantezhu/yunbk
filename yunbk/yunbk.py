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

    # 临时根目录
    tmp_root_dir = None

    # 之前的cwd目录保存起来
    old_work_dir = None
    # 临时工作区
    tmp_work_dir = None

    def __init__(self, backup_name, backends, keeps=None, tmp_root_dir=None):
        self.backup_name = backup_name
        self.backends = backends
        self.keeps = keeps
        self.dir_prefix = "{0}_".format(backup_name)
        self.tmp_root_dir = tmp_root_dir or constants.TMP_ROOT_DIR

    def __enter__(self):
        """Save the old current working directory,
            create a temporary directory,
            and make it the new current working directory.
        """
        self.old_work_dir = os.getcwd()
        self.tmp_work_dir = tempfile.mkdtemp(prefix=self.dir_prefix, dir=self.tmp_root_dir, suffix='_work')
        sh.cd(self.tmp_work_dir)
        logger.info("New current working directory: %s.", self.tmp_work_dir)
        return self

    def __exit__(self, type, value, traceback):
        """Reseting the current working directory,
            and run synchronization if enabled.
        """
        sh.cd(self.old_work_dir)
        logger.info("Back to %s", self.old_work_dir)
        shutil.rmtree(self.tmp_work_dir)

    def backup(self):
        """
        备份对应的path
        """

        now = datetime.datetime.now()
        str_now = now.strftime(constants.STRFTIME_TPL)

        # 临时tar包目录
        tmp_tar_dir = tempfile.mkdtemp(prefix=self.dir_prefix, dir=self.tmp_root_dir, suffix='_tar')

        tar_file_path = os.path.join(tmp_tar_dir, '%s.%s.tar.gz' % (self.backup_name, str_now))

        logger.info('tar_file_path: %s', tar_file_path)

        with tarfile.open(tar_file_path, "w:gz") as tar:
            tar.add(self.tmp_work_dir, os.path.basename(self.tmp_work_dir))

        try:
            for backend in self.backends:
                backend.upload(tar_file_path, self.backup_name)
        except Exception, e:
            raise e
        finally:
            shutil.rmtree(tmp_tar_dir)

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
