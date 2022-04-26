"""
自定义异常
"""


class GetSerializerError(Exception):
    """获取序列化器异常"""


class FlowNotClosedError(Exception):
    """
    jiandaoyun flow not closed
    2表示流程手动结束；1表示流程已完成；0表示流程进行中
    """
