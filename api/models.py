# from django.db import models
# from utils.common.models import TimeStampedModel
# from utils.common.constants import ENABLE_CHOICES, STATUS_ENABLE
#
#
# class UserPermissions(TimeStampedModel):
#     domain = models.CharField(verbose_name='域账号', max_length=30)
#     attr = models.CharField(verbose_name='属性名', max_length=20)
#     status = models.PositiveSmallIntegerField(verbose_name='状态', choices=ENABLE_CHOICES, default=STATUS_ENABLE)
#
#     class Meta:
#         verbose_name_plural = verbose_name = '- 用户权限'
#
#     def __str__(self):
#         return self.domain
