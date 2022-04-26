import logging
import types
from utils.env import env
from utils.wxwork import wechat_client

AGENT_ID = env.get('WX_AGENT_ID')
USER_IDS = env.get('MAINTAINERS')


def alert(self, level: int, msg: str, agent_id: str = None, user_ids=None):
    """
    参数类型参考 logger.log 方法
    @param: level 日志等级
    @param: msg: 日志内容
    @param: agent_id: 发送消息的企微应用 ID
    @param: user_ids: 接收消息的企微用户 id 列表
    """
    # 参数初始化
    agent_id = agent_id or AGENT_ID
    user_ids = user_ids or USER_IDS.split(';')

    self.log(level=level, msg=msg)
    wechat_client.message.send_text(agent_id=agent_id, user_ids=user_ids, content=msg)


logger = logging.getLogger('root')

# 动态给一个类实例添加类实例方法
logger.alert = types.MethodType(alert, logger)
