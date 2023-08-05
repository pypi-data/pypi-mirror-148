# from pprint import pprint

# from init_django import django_setup
#
# django_setup()
from django.db.models import ForeignKey, DecimalField, TextField, AutoField
from django_filters import DateTimeFilter, DateFilter, NumberFilter, ChoiceFilter, CharFilter, BooleanFilter, \
    MultipleChoiceFilter
from rest_framework.fields import MultipleChoiceField, ChoiceField, IntegerField, CharField, DateField, DateTimeField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import Serializer
from vue.utils import CustomBase64ImageField


def viewset_filter_beauty(viewset=None):
    """将viewset的过滤列表格式化为可读的字典"""
    filter_model = viewset.filter_class
    # 获取每个字段名和对应的label
    # print(filter_model.__dict__)
    # 获取所有的filter
    all_filters = filter_model.base_filters

    field_model = filter_model.Meta.model

    res = []

    field_type_map = {
        DateTimeFilter: "datetime",
        DateFilter: "date",
        NumberFilter: "number",
        ChoiceFilter: "choice",
        CharFilter: "char",
        BooleanFilter: "bool",
        MultipleChoiceFilter: "multi_choice",

    }

    for field in all_filters:
        # print("field", field, type(field), all_filters[field],type(all_filters[field]))

        field_class = all_filters[field]
        field_type = field_type_map.get(field_class.__class__)
        # 获取到真实的label 链式查询改为 .
        actual_field = field.replace("__", ".")  # 统一重写链式查询的字段 减少前端出错几率

        item = {"field_name": field, "field_type": field_type, "label": field}
        try:
            if "." not in actual_field:
                item["label"] = all_filters[field]._label or field_model._meta.get_field(field).verbose_name
        except Exception as e:
            pass

        if field_type == "choice":
            item["choice_text"] = str(field_model._meta.get_field(field)).lower().replace('.', '_')
        res.append(item)
    # print(res)

    return res


def filter_dict_to_vue(filter_dict):
    """将filter生成用户的vue代码"""
    from jinja2 import Environment, PackageLoader
    env = Environment(loader=PackageLoader('vue', 'templates'))
    template = env.get_template('list_filter_template.vue')
    with open('vue/templates/list_filter_template.vue', 'r', encoding='utf-8') as f:
        res = template.render(table=filter_dict)
        # print("vue_template:", res)
        return res


def filter_to_vue(viewset):
    try:
        filter_dict = viewset_filter_beauty(viewset)
        return filter_dict_to_vue(filter_dict)
    except:
        return ""


def field_re_format(key, field, field_model):
    """从field从抽取必要的字段 其他字段忽略"""
    field_type_map = {
        CharField: "char",
        ChoiceField: "choice",
        DateTimeField: "datetime",
        DateField: "date",
        MultipleChoiceField: "multi_choice",
        IntegerField: "int",
        DecimalField: "char",
        CustomBase64ImageField: "image",
        PrimaryKeyRelatedField: "foreign_key",
    }
    field_type = field_type_map.get(field.__class__)

    if not field.read_only:
        item = {"label": field.label, "field_name": key, "field_type": field_type, "required": field.required}
        try:
            item["max_length"] = field.max_length
        except:
            pass
    else:
        item = {"label": field.label, "field_name": key, "field_type": field_type, "read_only": True}

    if field_type == "choice":
        item["choice_text"] = str(field_model._meta.get_field(key)).lower().replace('.', '_')

    return item


def fill_field(main_part, all_fields, parent_source=None, pre_key=None, field_model=None):
    # print("parent_source",parent_source)
    for key in all_fields:
        field = all_fields[key]
        # print("field", field)
        if isinstance(field, (Serializer,)):
            # print("嵌套组件", field)
            child_fields = field.get_fields()
            if parent_source and not pre_key:
                main_part[parent_source][field.source] = {}
                fill_field(main_part, child_fields, parent_source=field.source, pre_key=parent_source,
                           field_model=field.Meta.model)

            elif parent_source and pre_key:
                main_part[parent_source] = {}
                main_part[parent_source][field.source] = {}
                fill_field(main_part, child_fields, parent_source=field.source, pre_key=parent_source,
                           field_model=field.Meta.model)
            else:
                main_part[field.source] = {}
                fill_field(main_part, child_fields, parent_source=field.source, field_model=field.Meta.model)

        else:
            # print("非嵌套", field, field.label)
            if not parent_source:
                main_part[key] = field_re_format(key, field, field_model)
            elif not pre_key:
                main_part[parent_source][key] = field_re_format(key, field, field_model)
            else:
                main_part[pre_key][parent_source][key] = field_re_format(key, field, field_model)


def viewset_ser_beauty(viewset=None):
    """将viewset的序列化器转换为可读的结构 进行分板块展示"""
    ser = viewset.serializer_class()  # 这里需要考虑嵌套nest serilizer的情况

    main_part = {}
    # print("ser_dict",ser.get_fields())
    all_fields = ser.get_fields()

    fill_field(main_part, all_fields, field_model=ser.Meta.model)

    # print(main_part)

    return main_part


def ser_dict_to_vue(table_name, ser_dict):
    from jinja2 import Environment, PackageLoader
    env = Environment(loader=PackageLoader('vue', 'templates'))
    template = env.get_template('detail_template.vue')
    with open('vue/templates/detail_template.vue', 'r', encoding='utf-8') as f:
        res = template.render(table=ser_dict, table_name=table_name)
        # print("vue_template:", res)
        return res


def viewset_to_vue(viewset):
    ser_dict = viewset_ser_beauty(viewset)
    return ser_dict_to_vue(ser_dict=ser_dict, table_name=viewset.serializer_class.Meta.model.Meta.verbose_name)


# if __name__ == '__main__':
#     # from health_plan.rest.api import ClientBuyInfoViewSet
#     # viewset_to_vue(ClientBuyInfoViewSet)
#     filter_to_vue(ClientBuyInfoViewSet)
