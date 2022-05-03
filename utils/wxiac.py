import requests
from utils.cache import cache_function
from utils.logger import logger
from api.constants import USER_PERMISSIONS, IAC_SECRET


class WxIAC(object):

    @staticmethod
    @cache_function(timeout=60 * 60 * 2)
    def get_access_token(appid: str, secret: str) -> str:
        """
        @param appid: 应用 ID
        @param secret: IAC 认证秘钥
        """
        url = "https://itapis.cvte.com/iac/app/access_token"

        params = {
            'appid': appid,
            'secret': secret
        }
        response = requests.get(url=url, params=params)
        json_response = response.json()
        logger.info(f'iac get access token: {json_response}')
        return json_response['data']['accessToken']

    """
    @param domain: 域账户
    """

    def get_user_info(self, domain: str) -> dict:
        url = "http://wx-api.gz.cvte.cn/user/search"
        headers = {
            'access-token': self.get_access_token(IAC_SECRET.get('appid'), IAC_SECRET.get('secret'))
        }
        params = {
            'data': domain
        }
        response = requests.get(url=url, headers=headers, params=params)
        json_response = response.json()
        logger.info(f'get user {domain} info: {json_response}')
        # 判断wxId是否为空
        for key in json_response['data']:
            if json_response['data'][key] is None:
                logger.info(f'get user {domain} info: wxId is None')
                wx_id = None
                break
            else:
                wx_id = json_response['data']['data']['wxId']
                break
        return wx_id


iac = WxIAC()
