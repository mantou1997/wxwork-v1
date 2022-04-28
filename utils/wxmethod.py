from utils.logger import logger

class WxMethod(object):

    def replace_zyz(self,extattr_add: dict, domain_p: str,content:str,option: str) -> dict:
        # 1. 判断attrs是否为空
        if not extattr_add['attrs']:
            logger.info(f'get attrs {domain_p} info: attrs is None,been added')
            extattr_add['attrs'] = [{'name': '志愿者', 'value': '', 'type': 0, 'text': {'value': ''}}]

        # 2.判断 志愿者 是否为空
        isOkZyz = '0'
        for item in extattr_add['attrs']:
            # 更新
            if item["name"] == "志愿者":
                isOkZyz = '1'
                # print("有志愿者")
                break
        if isOkZyz == '0':
            extattr_add['attrs'] = [{'name': '志愿者', 'value': '', 'type': 0, 'text': {'value': ''}}]
            logger.info(f'get 志愿者 {domain_p} info: attrs is None,been added')

        # 3.添加星星
        for itemm in extattr_add['attrs']:
            if itemm['name'] == '志愿者':
                extattr_add['attrs'] = [{'name': '志愿者', 'value': content, 'type': 0, 'text': {'value': content}}]

        return extattr_add


wx_method = WxMethod()
'''
# 志愿者 字段 替换
def replace_zyz(extattrAdd, cn_name, content):
    # 1. 判断attrs是否为空
    if not extattrAdd['attrs']:
        print(cn_name + '===========用户attrs为空')
        extattrAdd['attrs'] = [{'name': '志愿者', 'value': '', 'type': 0, 'text': {'value': ''}}]

    # 2.判断 志愿者 是否为空
    isOkZyz = '0'
    for item in extattrAdd['attrs']:
        # 更新
        if item["name"] == "志愿者":
            isOkZyz = '1'
            # print("有志愿者")
            break
    if isOkZyz == '0':
        extattrAdd['attrs'] = [{'name': '志愿者', 'value': '', 'type': 0, 'text': {'value': ''}}]
        print(cn_name + '=====无志愿者属性，已添加')

    # 3.添加星星
    for itemm in extattrAdd['attrs']:
        if itemm['name'] == '志愿者':
            extattrAdd['attrs'] = [{'name': '志愿者', 'value': content, 'type': 0, 'text': {'value': content}}]

    return extattrAdd
'''