from logging import ERROR
import openpyxl
from rest_framework.exceptions import ValidationError
from wechatpy.work import WeChatClient

from utils.wxiac import iac
from utils.logger import logger
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers import UpdateAttrSerializer
from rest_framework.viewsets import GenericViewSet
from api.constants import USER_PERMISSIONS


# Create your views here.
class MyExcelView(GenericViewSet):
    # url http://127.0.0.1:8000/v1/api/wx/extrattr/
    @action(methods=['post'], detail=False, url_path='extrattr')
    def myexcel(self, request, *args, **kwargs) -> Response:
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
        domain = data['domain']
        excel = data['excel']

        # 1.判断用户是否有权限

        # 1。获取token
        appid = 'db723212-3835-46a8-96d0-e760114dc0fb'
        secret = '7c625c45-a2b7-40db-a4ed-cc63d34e4d8a'
        token = iac.get_access_token(appid, secret)

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

            print(domain_p, field, content, option)
            # 3.根据域账户获取wx-id
            wx_id = iac.get_user_info(domain=domain)
            if not wx_id:
                continue

            """
            @param corp_id: 企业微信 corp
            @param secret: 密钥
            """
            corp_id = 'wx1deaa225db7d8ad5'
            secret = 'k17z57QaTptGQseICE2xZ7jde9H2VklMdHr1Ju8KgbE'
            # 4.调用企业微信API,获取extattr
            client = WeChatClient(corp_id, secret)
            get = client.user(wx_id)
            print(get)
            #extattrAdd = WeChatClient(corp_id, secret).user.get(wx_id)['extattr']
            #logger.info(f'get extattr {domain_p} info: {extattrAdd}')
            # 调用具体字段-方法



        wb.close()
        return Response({'11': '111'})


'''
class UpdateAttrViewSet(GenericViewSet):

    @action(methods=['POST'], detail=False, url_path='extrattr')
    def update_attrs(self, request, *args, **kwargs) -> Response:
        """"""
        # 0. 数据校验
        try:
            serializer = UpdateAttrSerializer(request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.data
        except ValidationError as e:
            errors = f'UpdateAttr Validate Failed: {e}'
            logger.alert(level=ERROR, msg=errors)
            return Response({"result": "failed", "message": errors})

        # 1.
        domain = data['domain']
        excel = data['excel']

        # 2.
        # with openpyxl.load_workbook() as wb:
        #     sheet1 = wb.get_sheet_by_name(wb.get_sheet_names()[0])
        #     for row in range(1, sheet1.max_row + 1):
        #         name = sheet1.cell(row=row, column=0).value
        #         cn_name = sheet1.cell(row=row, column=1).value
        #         content = sheet1.cell(row=row, column=2).value
        #
        #         wx_id = iac.get_user_info(domain=domain)

        return Response({'result': 'success'})
'''
