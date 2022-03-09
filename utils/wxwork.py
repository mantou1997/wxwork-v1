from wechatpy.enterprise import WeChatClient
from wechatpy.session.memorystorage import MemoryStorage
from utils.env import env

API_KEY = env.get('API_KEY')
CORPID = env.get('CORPID')
CORPSECRET = env.get('CORPSECRET')

session_interface = MemoryStorage()

wechat_client = WeChatClient(corp_id=CORPID, secret=CORPSECRET, session=session_interface)
