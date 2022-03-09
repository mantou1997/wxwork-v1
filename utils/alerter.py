from wechatpy.enterprise import WeChatClient
from utils.env import env

CORPID = env.get('CORPID')
CORPSECRET = env.get('ALERTSECRET')
ALERTID = env.get('ALERTID')

alerter = WeChatClient(corp_id=CORPID, secret=CORPSECRET)
