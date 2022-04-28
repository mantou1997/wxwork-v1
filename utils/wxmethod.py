from utils.logger import logger
from wechatpy.work import WeChatClient
from api.constants import USER_PERMISSIONS


class WxMethod(object):

    @staticmethod
    def replace_zyz(extattr_add: dict, domain_p: str, content: str) -> dict:
        # 1. 判断attrs是否为空
        if not extattr_add['attrs']:
            logger.info(f'get attrs {domain_p} info: attrs is None,been added')
            extattr_add['attrs'] = [{'name': '志愿者', 'value': '', 'type': 0, 'text': {'value': ''}}]

        # 2.判断 志愿者 是否为空
        is_ok = '0'
        for item in extattr_add['attrs']:
            # 更新
            if item["name"] == "志愿者":
                is_ok = '1'
                # print("有志愿者")
                break
        if is_ok == '0':
            extattr_add['attrs'] = [{'name': '志愿者', 'value': '', 'type': 0, 'text': {'value': ''}}]
            logger.info(f'get 志愿者 {domain_p} info: attrs is None,been added')

        # 3.添加星星
        for item in extattr_add['attrs']:
            if item['name'] == '志愿者':
                extattr_add['attrs'] = [{'name': '志愿者', 'value': content, 'type': 0, 'text': {'value': content}}]

        return extattr_add

    @staticmethod
    def replace_auth(extattr_add: dict, domain_p: str, content: str) -> dict:
        # 1. 判断attrs是否为空
        if not extattr_add['attrs']:
            logger.info(f'get attrs {domain_p} info: attrs is None,been added')
            extattr_add['attrs'] = [{'name': '认证', 'value': '', 'type': 0, 'text': {'value': ''}}]

        # 2.判断 认证 是否为空
        is_ok = '0'
        for item in extattr_add['attrs']:
            # 更新
            if item["name"] == "认证":
                is_ok = '1'
                # print("有志愿者")
                break
        if is_ok == '0':
            extattr_add['attrs'] = [{'name': '认证', 'value': '', 'type': 0, 'text': {'value': ''}}]
            logger.info(f'get 认证 {domain_p} info: attrs is None,been added')

        # 3.添加星星
        for item in extattr_add['attrs']:
            if item['name'] == '认证':
                extattr_add['attrs'] = [{'name': '认证', 'value': content, 'type': 0, 'text': {'value': content}}]

        return extattr_add

    @staticmethod
    def replace_gs(extattr_add: dict, domain_p: str, content: str) -> dict:
        # 1. 判断attrs是否为空
        if not extattr_add['attrs']:
            logger.info(f'get attrs {domain_p} info: attrs is None,been added')
            extattr_add['attrs'] = [{'name': '归属', 'value': '', 'type': 0, 'text': {'value': ''}}]

        # 2.判断 归属 是否为空
        is_ok = '0'
        for item in extattr_add['attrs']:
            # 更新
            if item["name"] == "归属":
                is_ok = '1'
                # print("有志愿者")
                break
        if is_ok == '0':
            extattr_add['attrs'] = [{'name': '归属', 'value': '', 'type': 0, 'text': {'value': ''}}]
            logger.info(f'get 归属 {domain_p} info: attrs is None,been added')

        # 3.添加星星
        for item in extattr_add['attrs']:
            if item['name'] == '归属':
                extattr_add['attrs'] = [{'name': '归属', 'value': content, 'type': 0, 'text': {'value': content}}]

        return extattr_add

    def update_api(self, extattr_add: dict, domain_p: str, field: str, content: str) -> dict:
        # 调用具体字段-方法
        if field == '志愿者':
            extattr_add_update = self.replace_zyz(extattr_add, domain_p, content)
        elif field == '认证':
            extattr_add_update = self.replace_auth(extattr_add, domain_p, content)
        elif field == '归属':
            extattr_add_update = self.replace_gs(extattr_add, domain_p, content)
        else:
            logger.info(f'{domain_p} :没有该字段')

        return extattr_add_update


wx_method = WxMethod()
'''
    @staticmethod
    def update_api(corp_id: str, secret: str, domain_p: str, domain: str, field: str, wx_id: str, content: str,
                   option: str) -> bool:
        extattr_add_update = []
        client = WeChatClient(corp_id, secret)
        extattr_add = client.user.get(wx_id)['extattr']
        logger.info(f'get extattr {domain_p} info: {extattr_add}')

        # 调用具体字段-方法
        if field == '志愿者' and (domain in USER_PERMISSIONS[field]):
            extattr_add_update = wx_method.replace_zyz(extattr_add, domain_p, content)
        elif field == '认证' and (domain in USER_PERMISSIONS[field]):
            extattr_add_update = wx_method.replace_auth(extattr_add, domain_p, content)
        elif field == '归属' and (domain in USER_PERMISSIONS[field]):
            extattr_add_update = wx_method.replace_gs(extattr_add, domain_p, content)
        else:
            logger.info(f'{domain_p} :没有该字段 or {domain}无权限操作 ')

        return extattr_add
        try:
            client.user.update(user_id=wx_id, extattr=extattr_add_update)
            logger.info(f'replace {field}\000 {domain_p} info: success')
            return True
        except:
            logger.info(f'replace {field}\000 {domain_p} info: error')
            return False

'''
