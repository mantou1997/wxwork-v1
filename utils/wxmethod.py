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

    def choice_option_field(self, option: str, extattr_add: dict, domain_excel: str, field: str, content: str) -> dict:
        """
        @param option: 选项： 替换/更新
        @param extattr_add: 企业微信个人信息
        @param domain_excel: excel里的域账户
        @param field: 修改的字段
        @param content: 修改的内容
        方法：先根据 option 判断操作（替换/更新），再根据 field 判断要修改那个字段
        """

        # 先判断企业微信 extattr_add 字典里的对应属性是否是空值
        self.is_none(extattr_add, domain_excel, field)

        if option == '删除' and content is not None:
            extattr_add = self.del_content(extattr_add, field, content)
        if option == '替换' or content is None:
            extattr_add = self.replace(extattr_add, field, content)
        if option == "新增" and content is not None:
            extattr_add = self.add(extattr_add, field, content)
        return extattr_add

    @staticmethod
    def del_content(extattr_add: dict, field: str, content: str) -> dict:
        """
        @param field: 要操作的字段
        @param extattr_add: 企业微信个人信息
        @param content: 删除的内容
        删除方法
        """
        # 1.切割content， 认证导师+面试导师 -> ['认证导师','面试导师']
        content_split = str(content).split("+")
        # 2.循环切割后的列表，获得每个值
        for content_item in content_split:
            # 3.获取对应 field 字段
            for item in extattr_add['attrs']:
                if item['name'] == field:
                    # 切割原有，判断删除内容是否已经存在原有数据里，如果不存在则 break
                    split = str(item["text"]["value"]).split("+")
                    if content_item not in split:
                        break

                    # 删除
                    [split.remove(cs) for cs in content_split]

                    # 删除后拼接
                    content_del = '+'.join(split)

                    extattr_add['attrs'] = [{'name': field, 'value': content_del, 'type': 0,
                                             'text': {'value': content_del}}]
                    return extattr_add

    @staticmethod
    def replace(extattr_add: dict, field: str, content: str) -> dict:
        """
        @param field: 要操作的字段
        @param extattr_add: 企业微信个人信息
        @param content: 修改的内容
        替换方法
        """

        # 3.添加值
        for item in extattr_add['attrs']:
            if item['name'] == field:
                extattr_add['attrs'] = [{'name': field, 'value': content, 'type': 0, 'text': {'value': content}}]

        return extattr_add

    @staticmethod
    def add(extattr_add: dict, field: str, content: str) -> dict:
        """
        @param field: 要操作的字段
        @param extattr_add: 企业微信个人信息
        @param content: 新增的内容
        新增方法
        """
        # 1.切割context， 认证导师+面试导师 -> ['认证导师','面试导师']
        content_split = str(content).split("+")
        # 2.循环切割后的列表，获得每个值
        for content_item in content_split:
            # 3.获取对应 field 字段
            for item in extattr_add['attrs']:
                if item['name'] == field:
                    # 切割原有，判断新增内容是否已经存在原有数据里，如果存在则 break
                    split = str(item["text"]["value"]).split("+")
                    if content_item in split:
                        break

                    # 判断是不是第一次新增，不是则拼接 + 号
                    if item["text"]["value"] != '':
                        content_item = '+' + content_item

                    extattr_add['attrs'] = [{'name': field, 'value': content_item, 'type': 0,
                                             'text': {'value': str(item["text"]["value"]) + content_item}}]

        return extattr_add

    @staticmethod
    def is_none(extattr_add, domain_excel, field):
        """
        @param field: 要操作的字段
        @param extattr_add: 企业微信个人信息
        @param domain_excel: excel里的域账户
        判断企业微信 extattr_add 字典里的对应属性是否是空值
        """

        # 1. 判断attrs是否为空，是空则添加
        if not extattr_add['attrs']:
            logger.info(f'get attrs {domain_excel} info: attrs is None,been added')
            extattr_add['attrs'] = [{'name': field, 'value': '', 'type': 0, 'text': {'value': ''}}]

        # 2.判断 field 字段 是否为空，是空则添加
        is_ok = '0'
        for item in extattr_add['attrs']:
            # 更新
            if item["name"] == field:
                is_ok = '1'
                break
        if is_ok == '0':
            extattr_add['attrs'] = [{'name': field, 'value': '', 'type': 0, 'text': {'value': ''}}]
            logger.info(f'get {field} {domain_excel} info: attrs is None,been added')


wx_method = WxMethod()
