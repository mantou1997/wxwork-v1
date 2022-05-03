from typing import Tuple, Any

from utils.logger import logger


class WxMethod(object):

    @staticmethod
    def get_excel_attr(ws: str, row: str) -> Tuple[Any, Any, Any, Any]:
        """
        @param ws: sheet1
        @param row: 行
        """
        domain_excel = ws.cell(row=row, column=2).value
        field = ws.cell(row=row, column=3).value
        content = ws.cell(row=row, column=4).value
        option = ws.cell(row=row, column=5).value
        return domain_excel, field, content, option

    @staticmethod
    def replace(extattr_add: dict, domain_excel: str, field: str, content: str) -> dict:
        """
        @param field: 要操作的字段
        @param extattr_add: 企业微信个人信息
        @param domain_excel: excel里的域账户
        @param content: 修改的内容
        方法：替换字段
        """

        # 1. 判断attrs是否为空
        if not extattr_add['attrs']:
            logger.info(f'get attrs {domain_excel} info: attrs is None,been added')
            extattr_add['attrs'] = [{'name': field, 'value': '', 'type': 0, 'text': {'value': ''}}]

        # 2.判断 field 字段 是否为空
        is_ok = '0'
        for item in extattr_add['attrs']:
            # 更新
            if item["name"] == field:
                is_ok = '1'
                break
        if is_ok == '0':
            extattr_add['attrs'] = [{'name': field, 'value': '', 'type': 0, 'text': {'value': ''}}]
            logger.info(f'get {field} {domain_excel} info: attrs is None,been added')

        # 3.添加值
        for item in extattr_add['attrs']:
            if item['name'] == field:
                extattr_add['attrs'] = [{'name': field, 'value': content, 'type': 0, 'text': {'value': content}}]

        return extattr_add

    def choice_option_field(self, option: str, extattr_add: dict, domain_excel: str, field: str, content: str) -> dict:
        """
        @param option: 选项： 替换/更新
        @param extattr_add: 企业微信个人信息
        @param domain_excel: excel里的域账户
        @param field: 修改的字段
        @param content: 修改的内容
        方法：先根据 option 判断操作（替换/更新），再根据 field 判断要修改那个字段
        """
        if option == '替换':
            extattr_add = self.replace(extattr_add, domain_excel, field, content)
            return extattr_add


wx_method = WxMethod()
