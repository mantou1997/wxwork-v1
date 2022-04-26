from rest_framework import serializers

from utils.drf.exceptions import FlowNotClosedError

# 简道云流程状态
CLOSED_MANUAL = 2
CLOSED_SUCCESS = 1
FLOW_WORKING = 0


class BaseSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class JDYBaseSerializer(BaseSerializer):
    """ 增加简道云流程状态的校验 """

    def to_internal_value(self, data):
        flow_state = data.get('flowState')
        if flow_state in [CLOSED_MANUAL, CLOSED_MANUAL, FLOW_WORKING]:
            data.update({'flow_state': flow_state})
        return data

    def validate(self, data):
        flow_state = data.get('flow_state')
        if flow_state in [CLOSED_MANUAL, FLOW_WORKING]:
            raise FlowNotClosedError("flow not closed success")
        return data

    def to_representation(self, instance):
        flow_state = instance.get('flowState')

        if flow_state in [CLOSED_MANUAL, CLOSED_SUCCESS, FLOW_WORKING]:
            instance.update({'flow_state': flow_state})
            del (instance['flowState'])

        return instance
