import json
import os

import requests
from eave import *
from rest_framework.fields import IntegerField, FloatField, DecimalField, BooleanField, empty

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ti.settings")
import django
django.setup()

from tickets.views import ProductLaunchApplyViewSet, ConsumerTrialApplyViewSet, ConsumerLaunchApplyViewSet, \
    VendorApplyViewSet, VendorApiApplyViewSet, TicketViewSet

LOCALHOST = 'http://127.0.0.1:8000'


def new_restful_apis(res_name, uri, view_set, localhost=LOCALHOST):

    # ======= GET =======
    api1 = Api()
    api1.title = '列出' + res_name
    api1.uri = uri
    api1.method = 'GET'

    api1.query_params = []
    filter_fields = view_set.filter_class.Meta.fields
    for field_name, kinds in filter_fields.items():
        for kind in kinds:
            query_name = f'{field_name}__{kind}'
            kind_zh = '筛选'
            if kind == 'exact':
                kind_zh = '指定'
                query_name = field_name
            elif kind in ['icontains', 'contains']:
                kind_zh = '匹配'
            elif kind == 'in':
                kind_zh = '命中'
            field_zh = view_set.queryset.model._meta.get_field(field_name).verbose_name
            description = kind_zh + field_zh
            api1.query_params.append(QP(name=query_name, description=description))

    url = localhost + api1.uri
    data = requests.get(url).json()
    if len(data['results']) > 2:
        data['results'] = [data['results'][0]]
    api1.response_example = json.dumps(data, ensure_ascii=False, indent=4)

    # ======= POST =======
    api2 = Api()
    api2.title = '创建' + res_name
    api2.uri = uri
    api2.method = 'POST'

    serializer = view_set.serializer_class()
    api2.body_params = []
    for field_name, field in serializer.fields.items():
        if field.read_only:
            continue
        type = 'string'
        if isinstance(field, IntegerField):
            type = 'int'
        elif isinstance(field, FloatField):
            type = 'float'
        elif isinstance(field, DecimalField):
            type = 'decimal'
        elif isinstance(field, BooleanField):
            type = 'bool'
        description = field.label
        if field.help_text:
            description += f'({field.help_text})'
        required = field.required
        default = field.default
        if default == empty:
            try:
                default = view_set.queryset.model._meta.get_field(field_name).default
            except:
                print(f'Warning: {field_name} field not found in f{view_set.queryset.model}!')
        api2.body_params.append(
            BP(name=field_name, type=type, description=description, required=required, default=default))

    if data['results']:
        api2.response_example = json.dumps(data['results'][0], ensure_ascii=False, indent=4)

    return api1, api2


doc = Doc(
    title='工单系统接口文档',
    version='1.0.0',
    host='http://172.23.43.15:8882',
    description='',
)


api1, api2 = new_restful_apis('用户测试申请', '/api/tickets/consumer_trial_apply/', ConsumerTrialApplyViewSet)
doc.apis.append(api1)
doc.apis.append(api2)

api1, api2 = new_restful_apis('用户上线申请', '/api/tickets/consumer_launch_apply/', ConsumerLaunchApplyViewSet)
doc.apis.append(api1)
doc.apis.append(api2)

api1, api2 = new_restful_apis('第三方供应商注册申请', '/api/tickets/vendor_apply/', VendorApplyViewSet)
doc.apis.append(api1)
doc.apis.append(api2)


api1, api2 = new_restful_apis('第三方API接入申请', '/api/tickets/vendor_api_apply/', VendorApiApplyViewSet)
doc.apis.append(api1)
doc.apis.append(api2)

api1, api2 = new_restful_apis('产品上线申请', '/api/tickets/product_launch_apply/', ProductLaunchApplyViewSet)
doc.apis.append(api1)
doc.apis.append(api2)

api1, api2 = new_restful_apis('工单', '/api/tickets/ticket/', TicketViewSet)
doc.apis.append(api1)
doc.apis.append(api2)

doc.build('api.html', 'zh')
