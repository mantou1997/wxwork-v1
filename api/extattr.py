from logging import ERROR

import openpyxl
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from wechatpy.work import WeChatClient

from api.constants import WX_SECRET, USER_PERMISSIONS
from api.serializers import UpdateAttrSerializer
from utils.logger import logger
from utils.wxiac import iac
from utils.wxmethod import wx_method


# Create your views here.123
class UpdateExtattrViewSet(GenericViewSet):
    # url http://127.0.0.1:8000/v1/api/wx/extrattr/
    @action(methods=['post'], detail=False, url_path='extattr')
    def update_extattr(self, request, *args, **kwargs) -> Response:
        # 0. 数据校验
        try:
            serializer = UpdateAttrSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            errors = f'UpdateAttr Validate Failed: {e}'
            logger.alert(level=ERROR, msg=errors)
            return Response({"result": "failed", "message": errors})
        domain: str = request.data['domain']
        excel = request.data['excel']

        wb = openpyxl.load_workbook(excel)
        ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])

        # 1.循环excel的每一行，修改企业微信信息
        for row in range(2, ws.max_row + 1):
            domain_excel, field, content, option = wx_method.get_excel_attr(ws, row)

            # 2.验证 field 字段是否正确，执行者是否有权限
            if field not in USER_PERMISSIONS or domain not in USER_PERMISSIONS[field]:
                logger.info(f'{domain_excel} 的{field}字段不合法')
                return Response({'message': f'1.{domain_excel} 域账户的({field})字段不合法。2.执行用户：{domain} ，对{field}字段没有权限修改'},
                                status=status.HTTP_404_NOT_FOUND)

            # 3.根据域账户获取wx-id
            wx_id = iac.get_user_info(domain=domain_excel)
            if not wx_id:
                logger.info(f'{domain_excel} :not wx_id ')
                continue

            # 4.调用企业微信api获取用户信息
            client = WeChatClient(WX_SECRET.get('corp_id'), WX_SECRET.get('secret'))
            extattr_add = client.user.get(wx_id)['extattr']
            logger.info(f'update extattr {domain_excel} info: {extattr_add}')

            # 5.先根据 option 判断操作（替换/更新），再根据 field 判断要修改那个字段
            extattr_add_update = wx_method.choice_option_field(option, extattr_add, domain_excel, field, content)

            try:
                # 6.调用企业微信api更改字段值
                client.user.update(user_id=wx_id, extattr=extattr_add_update)
                logger.info(f'{domain_excel} update success')
            except Exception as e:
                logger.info(f'{domain_excel} error: {e}')

        wb.close()
        return Response({'message': f'用户字段更新完成'}, status=status.HTTP_200_OK)
