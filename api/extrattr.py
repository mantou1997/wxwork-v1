from logging import ERROR
import openpyxl
from rest_framework.exceptions import ValidationError
from wechatpy.work import WeChatClient

from utils.wxiac import iac
from utils.wxmethod import wx_method
from rest_framework import status
from utils.logger import logger
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers import UpdateAttrSerializer
from rest_framework.viewsets import GenericViewSet

from api.constants import IAC_SECRET, WX_SECRET, USER_PERMISSIONS


# Create your views here.
class MyExcelView(GenericViewSet):
    # url http://127.0.0.1:8000/v1/api/wx/extrattr/
    @action(methods=['post'], detail=False, url_path='extattr')
    def my_excel(self, request, *args, **kwargs) -> Response:
        # 0. 数据校验
        try:
            # 获取前端传入的请求体数据
            data = request.data
            # 创建序列化器进行反序列化
            serializer = UpdateAttrSerializer(data=data)
            # 调用序列化器的is_valid方法进行校验
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            errors = f'UpdateAttr Validate Failed: {e}'
            logger.alert(level=ERROR, msg=errors)
            return Response({"result": "failed", "message": errors})
        domain: str = data['domain']
        excel = data['excel']

        # 1。获取token
        iac.get_access_token(IAC_SECRET.get('appid'), IAC_SECRET.get('secret'))

        """
        2.读取excel
        @param domain_p: 表单里的域账户信息
        @param field: 要修改的字段
        @param content: 修改的内容
        @param option: 执行的选项
        """
        wb = openpyxl.load_workbook(excel)
        ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])

        for row in range(2, ws.max_row + 1):
            domain_p = ws.cell(row=row, column=2).value
            field = ws.cell(row=row, column=3).value
            content = ws.cell(row=row, column=4).value
            option = ws.cell(row=row, column=5).value

            # 判断执行者是否有权限
            if domain not in USER_PERMISSIONS[field]:
                logger.info(f'{domain_p} :执行者没有权限')
                return Response({'message': f'{domain} :执行者没有权限'}, status=status.HTTP_404_NOT_FOUND)

            if content == "清空":
                content = ""

            # 3.根据域账户获取wx-id
            """
            @param wx_id: 企业微信 id
            """
            wx_id = iac.get_user_info(domain=domain_p)
            if not wx_id:
                logger.info(f'{domain_p} :not wx_id ')
                continue

            """
            @param corp_id: 企业微信 corp
            @param secret: 密钥
            @param extattr_add: 企业微信个人信息
            """
            client = WeChatClient(WX_SECRET.get('corp_id'), WX_SECRET.get('secret'))
            extattr_add = client.user.get(wx_id)['extattr']
            logger.info(f'get extattr {domain_p} info: {extattr_add}')

            # 根据用户需要修改的字段，调用具体的方法
            extattr_add_update = wx_method.update_api(extattr_add, domain_p, field, content)
            try:
                # 调用企业微信更改字段值
                client.user.update(user_id=wx_id, extattr=extattr_add_update)
            except Exception as e:
                logger.info(f'{domain_p} error: {e}')

        wb.close()
        return Response({'message': f'用户字段更新完成'}, status=status.HTTP_200_OK)


