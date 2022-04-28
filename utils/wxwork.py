from logging import Logger, getLogger

from wechatpy.work import WeChatClient
from utils.env import env

logger: Logger = getLogger('root')

WX_CORP_ID = env.get('WX_CORP_ID')
WX_CORP_SECRET = env.get('WX_CORP_SECRET')

WX_AGENT_ID = env.get('WX_AGENT_ID')
MAINTAINERS = env.get('MAINTAINERS').split(';')

wechat_client = WeChatClient(corp_id=WX_CORP_ID, secret=WX_CORP_SECRET)
