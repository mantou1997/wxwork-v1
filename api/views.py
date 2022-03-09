import logging
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from utils.wxwork import wechat_client
from utils.alerter import alerter, ALERTID
from api.serializers import TagSerializer
from api.constants import APP_TAG_MAP

logger = logging.getLogger('root')


class WxworkTag(GenericViewSet):
    serializer_class = TagSerializer

    @action(methods=['POST'], detail=False)
    def add_user(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data['data'])
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            user_id = request.data['data']['user']['username']
            alerter.message.send_text(agent_id=ALERTID, user_ids=[user_id], content=str(e))
            return Response({'status': 'error', 'message': f'validate error: {e}'}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.data
        for app in data.get('apps'):
            tag_id = APP_TAG_MAP.get(app)
            user_id = data['user']['username']
            response = wechat_client.tag.add_users(tag_id=tag_id, user_ids=[user_id])
            if response['errcode'] == 0 and response['errmsg'] == 'ok':
                alerter.message.send_text(agent_id=ALERTID, user_ids=[user_id], content=f'{app} 应用权限已开通，请在企微工作台查看')
                logger.info(f'wxwork app <{app}> add user <{user_id}> with tag <{tag_id}>')
        return Response({'status': 'success', 'message': 'tag add user success'})
