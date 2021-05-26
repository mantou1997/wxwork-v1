import json

import requests
from django.conf import settings

from utils.cache import cache_function


def get_user_ad_info(users) -> dict:
    """
    通过域账号获取 AD 信息
    @param users: 逗号分隔的字符串; ex:  aaa,bbb,ccc
    """
    url = "https://itgw.cvte.com/env-101/infra/public/ad/v1/user/"
    return requests.get(url=url,
                        headers={"apikey": settings.API_KEY},
                        params={"accounts": users}).json()


@cache_function(key='wx_access_token', timeout=2 * 60 * 60)
def get_access_token() -> str:
    """获取 access token """
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    response = requests.get(url=url,
                            params={
                                "corpid": settings.CORPID,
                                "corpsecret": settings.CORPSECRET
                            }).json()
    return response['access_token']


def update_wx_user(userid: str, extattr: dict):
    """
    更新企微用户信息
    @param: userid: 用户企业微信 id
    @param: extattr: 扩展字段
    """
    url = "https://qyapi.weixin.qq.com/cgi-bin/user/update"
    access_token = get_access_token()
    requests.post(url=url,
                  params={
                      "access_token": access_token
                  },
                  data=json.dumps({
                      "userid": userid,
                      "extattr": extattr
                  }))
