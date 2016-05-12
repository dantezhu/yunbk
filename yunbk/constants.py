# -*- coding: utf-8 -*-

# 转化成time的格式
STRFTIME_TPL = '%Y%m%d_%H%M%S'

# 需要保留的时间
# 看源码可知，是用如下代码实现的:
#    return (filters.Years.filter(datetimes, number=years, now=now) |
#            filters.Months.filter(datetimes, number=months, now=now) |
#            filters.Weeks.filter(datetimes, number=weeks,
#                                 firstweekday=firstweekday, now=now) |
#            filters.Days.filter(datetimes, number=days, now=now) |
#            filters.Hours.filter(datetimes, number=hours, now=now) |
#            filters.Minutes.filter(datetimes, number=minutes, now=now) |
#            filters.Seconds.filter(datetimes, number=seconds, now=now))
# 比如 days=1，由于days的mark会替换hours之类的都为0，所以就代表保留最近一天的第一个
# 又比如 days=1, hours=2，则代表保留最近一天的第一个，以及最近两小时的第一个
# years 和 months 会不太一样，具体参考其每个的mark函数
# 所以下面的写法，相当于保存: 最近3个月的每月第一个，最近4周的每周第一个，最近7天的每天第一个，最近3600*24秒的的每秒第一个
# 即一天内多个的话，会被删除为只剩下第一个

# 已验证，确实是第一个而不是最后一个
KEEPS_NORMAL = dict(
    months=3,
    weeks=4,
    days=7,
    seconds=3600*24,
)
