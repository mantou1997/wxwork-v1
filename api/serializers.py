from rest_framework import serializers
from utils.drf.serializers import JDYBaseSerializer, BaseSerializer


class StringListField(serializers.ListSerializer):
    child = serializers.CharField()

    def update(self, instance, validated_data):
        pass


class TagSerializer(JDYBaseSerializer):
    user = serializers.JSONField(label='用户', required=True)
    apps = StringListField(label='应用', required=True)
    flow_state = serializers.IntegerField(label='流程状态', required=True)


class UpdateAttrSerializer(BaseSerializer):
    domain = serializers.CharField(label='域账号', max_length=20)
    excel = serializers.FileField(label='文件', max_length=200)
