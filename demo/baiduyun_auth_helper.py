# -*- coding: utf-8 -*-
"""
参照文档: http://developer.baidu.com/wiki/index.php?title=docs/oauth/authorization
"""

import urllib

client_id = ''
client_secret = ''
auth_code = ''


print 'https://openapi.baidu.com/oauth/2.0/authorize' + '?' + urllib.urlencode(dict(
    client_id=client_id,
    response_type='code',
    redirect_uri='oob'
))

print 'https://openapi.baidu.com/oauth/2.0/token' + '?' + urllib.urlencode(dict(
    grant_type='authorization_code',
    code=auth_code,
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri='oob',
))
