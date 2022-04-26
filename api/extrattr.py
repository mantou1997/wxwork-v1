from logging import ERROR
import openpyxl
from rest_framework.exceptions import ValidationError
from utils.wxiac import iac
from utils.logger import logger
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers import UpdateAttrSerializer
from rest_framework.viewsets import GenericViewSet
from api.constants import USER_PERMISSIONS


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
