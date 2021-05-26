from import_export import fields
from import_export import resources
from import_export import widgets
from taggit.forms import TagField
from taggit.models import Tag

from wxtags.models import KEY_CHOICES
from wxtags.models import WxTags


def get_key_from_value(value):
    for item in KEY_CHOICES:
        k, v = item
        if v == value.strip():
            return k
    raise Exception('No Key Found')


def get_value_by_key(key):
    for item in KEY_CHOICES:
        k, v = item
        if k == key:
            return v
    raise Exception('No Value for Key %d' % key)


class TagWidget(widgets.ManyToManyWidget):
    def render(self, value, obj=None):
        return self.separator.join(
            [obj.name for obj in value.all()]
        )

    def clean(self, value, row=None, *args, **kwargs):
        values = TagField().clean(value)
        # return [
        #     Tag.objects.get_or_create(name=tag)[0]
        #     for tag in values
        # ]
        tags = list()
        for value in values:
            for tag in value.split(";"):
                t, _ = Tag.objects.get_or_create(name=tag)
                tags.append(t)
        return tags


class TagFieldImport(fields.Field):
    """导入 tag 时自动转换"""

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
        row['key'] = get_key_from_value(row['key'])
