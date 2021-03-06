"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'config.grappelli.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import gettext_lazy as _

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        # 第一列: 站点模型
        self.children.append(modules.ModelList(
            _('用户自定义模型'),
            collapsible=True,
            column=1,
            css_classes=('collapse open',),
            # 此处添加模型列表
            models=[
                'account.models.User',
            ]
        ))

        self.children.append(modules.ModelList(
            _('标签管理'),
            collapsible=True,
            column=1,
            css_classes=('collapse open',),
            # 此处添加模型列表
            models=[
                'api.models.UserPermissions',
                'wxtags.models.WxTags',
                'taggit.models.Tag',
            ]
        ))

        # 第二列: 管理员权限
        self.children.append(modules.ModelList(
            _('管理员权限'),
            column=2,
            collapsible=True,
            models=('django.contrib.*',),
        ))

        self.children.append(modules.ModelList(
            _('周期性任务'),
            collapsible=True,
            column=2,
            css_classes=('collapse open',),
            models=['django_celery_beat.models.*']
        ))

        # 第三列: 第三方链接
        self.children.append(modules.LinkList(
            _('媒体文件管理'),
            column=3,
            children=[
                {
                    'title': _('FileBrowser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
            ]
        ))
