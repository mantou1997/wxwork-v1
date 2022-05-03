from utils.logger import logger

from api.constants import USER_PERMISSIONS


# from rest_framework import status
# from rest_framework.response import Response
# from wechatpy.work import WeChatClient


class WxMethod(object):

    @staticmethod
    def is_valid(field: str, domain: str, domain_excel: str):
        """
        @param field: 修改的字段
        @param domain: 修改的内容
        @param domain_excel: excel里的域账户
        """

        if field not in USER_PERMISSIONS:
            logger.info(f'{domain_excel} 的{field}字段不合法')
            return 'not_field'
        # 判断执行者是否有权限
        if domain not in USER_PERMISSIONS[field]:
            logger.info(f'{domain_excel} :执行者没有权限')
            return 'net_domain'

    @staticmethod
    # 替换-志愿者
    def replace(extattr_add: dict, domain_excel: str, field:str,content: str) -> dict:
        """
        @param field: 要操作的字段
        @param extattr_add: 企业微信个人信息
        @param domain_excel: excel里的域账户
        @param content: 修改的内容
        """

        # 1. 判断attrs是否为空
        if not extattr_add['attrs']:
            logger.info(f'get attrs {domain_excel} info: attrs is None,been added')
            extattr_add['attrs'] = [{'name': field, 'value': '', 'type': 0, 'text': {'value': ''}}]

        # 2.判断 志愿者 是否为空
        is_ok = '0'
        for item in extattr_add['attrs']:
            # 更新
            if item["name"] == field:
                is_ok = '1'
                # print("有志愿者")
                break
        if is_ok == '0':
            extattr_add['attrs'] = [{'name': field, 'value': '', 'type': 0, 'text': {'value': ''}}]
            logger.info(f'get {field} {domain_excel} info: attrs is None,been added')

        # 3.添加星星
        for item in extattr_add['attrs']:
            if item['name'] == field:
                extattr_add['attrs'] = [{'name': field, 'value': content, 'type': 0, 'text': {'value': content}}]

        return extattr_add

    @staticmethod
    # 替换-认证
    def replace_auth(extattr_add: dict, domain_excel: str, content: str) -> dict:
        """
        @param extattr_add: 企业微信个人信息
        @param domain_excel: excel里的域账户
        @param content: 修改的内容
        """

        # 1. 判断attrs是否为空
        if not extattr_add['attrs']:
            logger.info(f'get attrs {domain_excel} info: attrs is None,been added')
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
            logger.info(f'get 认证 {domain_excel} info: attrs is None,been added')

        # 3.添加星星
        for item in extattr_add['attrs']:
            if item['name'] == '认证':
                extattr_add['attrs'] = [{'name': '认证', 'value': content, 'type': 0, 'text': {'value': content}}]

        return extattr_add

    @staticmethod
    # 替换-归属
    def replace_gs(extattr_add: dict, domain_excel: str, content: str) -> dict:
        """
        @param extattr_add: 企业微信个人信息
        @param domain_excel: excel里的域账户
        @param content: 修改的内容
        """

        # 1. 判断attrs是否为空
        if not extattr_add['attrs']:
            logger.info(f'get attrs {domain_excel} info: attrs is None,been added')
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
            logger.info(f'get 归属 {domain_excel} info: attrs is None,been added')

        # 3.添加星星
        for item in extattr_add['attrs']:
            if item['name'] == '归属':
                extattr_add['attrs'] = [{'name': '归属', 'value': content, 'type': 0, 'text': {'value': content}}]

        return extattr_add

    def choice_option_field(self, option: str, extattr_add: dict, domain_excel: str, field: str, content: str) -> dict:
        """
        @param option: 操作： 替换/更新
        @param extattr_add: 企业微信个人信息
        @param domain_excel: excel里的域账户
        @param field: 修改的字段
        @param content: 修改的内容

        方法：先根据 option 判断操作（替换/更新），再根据 field 判断要修改那个字段
        """
        if option == '替换':
            extattr_add = self.replace(extattr_add, domain_excel, field, content)
            return extattr_add

    # 根据field，修改对应字段
    # def choice_field(self, extattr_add: dict, domain_excel: str, field: str, content: str) -> dict:
    #     """
    #     @param extattr_add: 企业微信个人信息
    #     @param domain_excel: excel里的域账户
    #     @param field: 修改的字段
    #     @param content: 修改的内容
    #     """
    #     extattr_add_update = {}
    #
    #     # 调用具体字段-方法
    #     if field == '志愿者':
    #         extattr_add_update = self.replace_zyz(extattr_add, domain_excel, content)
    #     elif field == '认证':
    #         extattr_add_update = self.replace_auth(extattr_add, domain_excel, content)
    #     elif field == '归属':
    #         extattr_add_update = self.replace_gs(extattr_add, domain_excel, content)
    #     else:
    #         logger.info(f'{domain_excel} :没有该字段')
    #
    #     return extattr_add_update


wx_method = WxMethod()
