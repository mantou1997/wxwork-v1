from django.conf import settings
from django.db import models
from model_utils.models import UUIDModel, TimeStampedModel
from taggit.managers import TaggableManager

from wxtags.constants import KEY_CHOICES, AUTHENTICATION


class WxTags(TimeStampedModel):
    """企业微信用户标签模型"""
    da = models.CharField(verbose_name='域账号', max_length=20)
    wxid = models.CharField(verbose_name='企微 ID', max_length=20, blank=True, null=True)
    key = models.PositiveSmallIntegerField(verbose_name='授权字段', choices=KEY_CHOICES, default=AUTHENTICATION)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='操作', on_delete=models.CASCADE, blank=True,
                                 null=True)
    tags = TaggableManager()

    class Meta:
        verbose_name_plural = verbose_name = '- 企微标签管理'

    def __str__(self):
        return self.da
