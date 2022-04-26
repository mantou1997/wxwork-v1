from logging import ERROR

from utils.drf.exceptions import FlowNotClosedError
from utils.logger import logger
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from utils.wxwork import wechat_client
from api.serializers import TagSerializer
from api.constants import APP_TAG_MAP


class WxworkTag(GenericViewSet):
    serializer_class = TagSerializer

    @action(methods=['POST'], detail=False)
    def add_user(self, request, *args, **kwargs):
        # 0. 数据校验
        try:
            serializer = self.get_serializer(data=request.data['data'])
            serializer.is_valid(raise_exception=True)
            data = serializer.data
        except FlowNotClosedError:
            return Response({"result": "failed", "message": 'flow not closed'})
        except ValidationError as e:
            errors = f'Wxwork Add Tag Validate Failed: {e}'
            logger.alert(level=ERROR, msg=errors)
            return Response({"result": "failed", "message": errors})

        # 1. 根据 APP 添加标签
        for app in data.get('apps'):
            tag_id = APP_TAG_MAP.get(app)
            user_id = data['user']['username']
            response = wechat_client.tag.add_users(tag_id=tag_id, user_ids=[user_id])
            if response['errcode'] == 0 and response['errmsg'] == 'ok':
                logger.alert(level=ERROR, msg=f'{app} 应用权限已开通，请在企微工作台查看', user_id=[user_id])
        return Response({'status': 'success', 'message': 'tag add user success'})
