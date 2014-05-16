# -*- coding: utf-8 -*-

import datetime
import constants
from grandfatherson import to_delete, to_keep


def filter_delete_filename_list(filename_list, keeps):
    """
    获取需要删除的
    """
    time_to_filename = dict()

    for filename in filename_list:
        slist = filename.split('.')
        if len(slist) < 2:
            #like yb.20140516_114126.tar
            continue

        str_datetime = slist[-2]

        dt = datetime.datetime.strptime(str_datetime, constants.STRFTIME_TPL)

        time_to_filename[dt] = filename

    # 要删除的时间，如果同一天有好多个的话，只保留第一个
    delete_times = to_delete(time_to_filename.keys(), **keeps)

    return [time_to_filename[it] for it in delete_times]
