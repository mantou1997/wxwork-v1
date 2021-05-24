from django import forms
from django.contrib import admin
from import_export import fields
from import_export import resources
from import_export import widgets
from import_export.admin import ImportExportModelAdmin
from import_export.forms import ImportForm, ConfirmImportForm
from taggit.forms import TagField
from taggit.models import Tag

from account.models import User
from wxtags.models import WxTags, KEY_CHOICES


class CustomImportForm(ImportForm):
    author = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True)


class CustomConfirmImportForm(ConfirmImportForm):
    author = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True)


class TagWidget(widgets.ManyToManyWidget):
    def render(self, value, obj=None):
        return self.separator.join(
            [obj.name for obj in value.all()]
        )

    def clean(self, value, row=None, *args, **kwargs):
        values = TagField().clean(value)
        return [
            Tag.objects.get_or_create(name=tag)[0]
            for tag in values
        ]


class TagFieldImport(fields.Field):

    def save(self, obj, data, is_m2m=False):
        if not self.readonly:
            attrs = self.attribute.split('__')
            for attr in attrs[:-1]:
                obj = getattr(obj, attr, None)
            cleaned = self.clean(data)
            if cleaned is not None or self.saves_null_values:
                if not is_m2m:
                    setattr(obj, attrs[-1], cleaned)
                else:
                    getattr(obj, attrs[-1]).set(*cleaned, clean=True)


class WxTagsResource(resources.ModelResource):
    """导入导出资源配置"""
    tags = TagFieldImport(attribute="tags", column_name="tags", widget=TagWidget(Tag, separator=";"))

    class Meta:
        model = WxTags
        import_id_fields = ['da']
        skip_unchanged = True
        report_skipped = True
        fields = ['da', 'wxid', 'key', 'operator__username']
        export_order = ['da', 'wxid', 'key', 'operator__username']

    @staticmethod
    def dehydrate_key(obj):
        return obj.get_key_display()

    def after_import_instance(self, instance, new, row_number=None, **kwargs):
        instance.operator = kwargs.get('user')

    def before_import_row(self, row, row_number=None, **kwargs):
        row['key'] = self.get_key_from_value(row['key'])

    @staticmethod
    def get_key_from_value(value):
        for item in KEY_CHOICES:
            k, v = item
            if v == value.strip():
                return k
        raise Exception('No Key Found')


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

    def save_model(self, request, obj, form, change):
        """保存模型时，自动填充 operator 字段"""
        obj.operator = request.user
        super(WxTagsAdmin, self).save_model(request, obj, form, change)

    @staticmethod
    def tag_list(obj):
        return u",".join(o.name for o in obj.tags.all())
