from rest_framework import serializers
from api.constants import APP_TAG_MAP


class StringListField(serializers.ListSerializer):
    child = serializers.CharField()

    def update(self, instance, validated_data):
        pass


class TagSerializer(serializers.Serializer):
    user = serializers.JSONField(label='用户', required=True)
    director = serializers.JSONField(label='主管', required=True)
    apps = StringListField(label='应用', required=True)

    def validate_apps(self, value):
        keys = APP_TAG_MAP.keys()
        if set(value).issubset(set(keys)):
            return value

        # 求差集
        diff = ','.join(list(set(value).difference(set(keys))))
        raise serializers.ValidationError(f'【{diff}】暂不支持，请联系管理员')

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
