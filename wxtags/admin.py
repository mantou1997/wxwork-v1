from django.contrib import admin
from django.contrib.admin.actions import delete_selected
from import_export.admin import ImportExportModelAdmin

from wxtags.models import WxTags
from wxtags.resources import WxTagsResource, get_value_by_key
from wxtags.utils import get_user_ad_info, update_wx_user

delete_selected.short_description = "❌ 删除所选对象"


@admin.register(WxTags)
class WxTagsAdmin(ImportExportModelAdmin):
    """企微字段管理"""
    list_display = ['da', 'wxid', 'key', 'tag_list', 'operator', 'created', 'modified']
    list_filter = ['key', 'operator__username']
    search_fields = ['da', 'tags', 'operator__username']
    fieldsets = [
        ('基本信息', {'classes': ['grp-collapse grp-open'],
                  'fields': ['da', 'wxid', 'key']}),
        ('标签管理', {'classes': ['grp-collapse grp-open'], 'fields': ['tags']}),
    ]
    resource_class = WxTagsResource
    actions = ['get_wxid_by_da', 'add_tag_by_user']

    def save_model(self, request, obj, form, change):
        """保存模型时，自动填充 operator 字段"""
        obj.operator = request.user
        super(WxTagsAdmin, self).save_model(request, obj, form, change)

    @staticmethod
    def tag_list(obj):
        return u",".join(o.name for o in obj.tags.all())

    def get_wxid_by_da(self, request, queryset):
        """通过域账号换取企业微信 ID"""
        das = ','.join([q.da for q in queryset.filter(wxid__isnull=True)])
        if not das:
            self.message_user(request, "没有用户需要获取企业微信 ID")
        else:
            try:
                results = get_user_ad_info(users=das)
                self.message_user(request, "共计查询: %d, 实际查询: %d" % (results['user_sum'], results['params_sum']))
                for item in results['data']:
                    queryset.filter(da=item['sAMAccountName']).update(wxid=item['serialNumber'])
            except Exception as e:
                self.message_user(request, e)

    get_wxid_by_da.short_description = '🔄 1. 获取微信 ID'

    def add_tag_by_user(self, request, queryset):
        """根据用户给企业微信打标签"""
        users = dict()
        # 数据去重
        for q in queryset.filter(wxid__isnull=False):
            users[q.wxid] = q.da

        # 循环
        for wxid, da in users.items():
            attrs = list()
            for q in queryset.filter(wxid=wxid):
                tags = [t.name for t in q.tags.all()]
                if tags:
                    key = get_value_by_key(q.key)
                    attr = {
                        "type": 0,
                        "name": key,
                        "text": {
                            "value": "|".join(tags)
                        }
                    }
                    attrs.append(attr)
            update_wx_user(userid=wxid, extattr={"attrs": attrs})

    add_tag_by_user.short_description = '🚀 2. 更新用户标签'
