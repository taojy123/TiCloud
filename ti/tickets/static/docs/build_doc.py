import json
import os

import requests
from eave import *
from rest_framework.fields import IntegerField, FloatField, DecimalField, BooleanField, empty

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ti.settings")
import django
django.setup()

from tickets.views import ProductLaunchApplyViewSet, ConsumerTrialApplyViewSet, VendorApplyViewSet, \
    VendorApiApplyViewSet, TicketViewSet, UserViewSet, ConsumerRegisterApplyViewSet, ConsumerOrderApplyViewSet

TESTHOST = 'http://127.0.0.1:8000'


def action_description_handle(description):
    description = description.strip()
    lines = description.splitlines()
    title = lines[0].strip()
    description = ''
    for line in lines[1:]:
        description += line.strip() + '\n\n'
    return title, description


def new_restful_apis(res_name, uri, view_set, testhost=TESTHOST):

    # ======= GET List =======
    api_list = Api()
    api_list.title = res_name + '列表'
    api_list.uri = uri
    api_list.method = 'GET'

    api_list.query_params = []
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
            api_list.query_params.append(QP(name=query_name, description=description))

    url = testhost + api_list.uri
    data = requests.get(url).json()
    if len(data['results']) > 2:
        data['results'] = [data['results'][0]]
    api_list.response_example = json.dumps(data, ensure_ascii=False, indent=4)

    # ======= POST =======
    api_post = Api()
    api_post.title = '创建' + res_name
    api_post.uri = uri
    api_post.method = 'POST'

    serializer = view_set.serializer_class()
    api_post.body_params = []
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
            description += f' [{field.help_text}]'
        required = field.required
        default = field.default
        if default == empty:
            try:
                default = view_set.queryset.model._meta.get_field(field_name).default
            except:
                # print(f'Warning: {field_name} field not found in {view_set.queryset.model}')
                pass
        api_post.body_params.append(
            BP(name=field_name, type=type, description=description, required=required, default=default))
    
    if data['results']:
        api_post.response_example = json.dumps(data['results'][0], ensure_ascii=False, indent=4)

    # ======= GET Detail =======
    api_detail = Api()
    api_detail.title = res_name + '详情'
    api_detail.uri = f'{uri.rstrip("/")}/<id>/'
    api_detail.method = 'GET'
    api_detail.uri_params = [UP(name='id', description=f'{res_name} ID', example=1)]

    url = testhost + uri
    data = requests.get(url).json()
    if data['results']:
        res_id = data['results'][0]['id']
        url = f'{url.rstrip("/")}/{res_id}/'
        data2 = requests.get(url).json()
        api_detail.response_example = json.dumps(data2, ensure_ascii=False, indent=4)
        
    # ======= Actions =======
    actions = []
    for item in dir(view_set):
        func = getattr(view_set, item)
        if not all([hasattr(func, 'detail'), hasattr(func, 'url_path'), hasattr(func, 'kwargs')]):
            continue
        detail = func.detail
        url_path = func.url_path
        description = func.kwargs['description']
        method = list(func.mapping.keys())[0].upper()
        title, description = action_description_handle(description)
        if detail:
            action_uri = f'{uri.rstrip("/")}/<id>/{url_path}/'
        else:
            action_uri = f'{uri.rstrip("/")}/{url_path}/'
            
        api_action = Api(title=title, uri=action_uri, method=method, description=description)
        actions.append(api_action)
        
    # ============================
    
    return api_list, api_post, api_detail, actions


doc = Doc(
    title='工单系统接口文档',
    version='1.0.0',
    host='http://172.23.43.15:8882',
)

doc.add_note(
    title='本系统使用 jwt 进行用户鉴权',
    content=f"""
需要登录权限的接口请将 `token` 添加至请求头部的 `Authorization` 中并附以 `JWT` 前缀, 例如:
```
curl -H "Authorization: JWT xxxxx.yyyy.zzzzz" {doc.host}/api/
```
""")

api = Api(
    title='用户登录',
    uri='/api/login/',
    method='POST',
    description='使用用户名密码登录系统，换取 token',
    body_params=[
        BP(name='username', description='用户名', required=True),
        BP(name='password', description='密码', required=True),
    ],
    response_example="""{"token": "xxxxx.yyyy.zzzzz"}""",
    tips='请在前端保存下返回的 `token`，之后每次请求接口时都需要将 `token` 置于请求头部的 `Authorization` 中',
)
doc.add_api(api)


api1, api2, api3, actions = new_restful_apis('系统用户', '/api/tickets/users/', UserViewSet)
doc.add_apis(api1, *actions)

api1, api2, api3, actions = new_restful_apis('用户注册申请', '/api/tickets/consumer_register_applies/', ConsumerRegisterApplyViewSet)
doc.add_apis(api2, api3, *actions)

api1, api2, api3, actions = new_restful_apis('用户订单申请', '/api/tickets/consumer_order_applies/', ConsumerOrderApplyViewSet)
doc.add_apis(api2, api3, *actions)

api1, api2, api3, actions = new_restful_apis('用户测试申请', '/api/tickets/consumer_trial_applies/', ConsumerTrialApplyViewSet)
doc.add_apis(api2, api3, *actions)

api1, api2, api3, actions = new_restful_apis('第三方供应商注册申请', '/api/tickets/vendor_applies/', VendorApplyViewSet)
doc.add_apis(api2, api3, *actions)

api1, api2, api3, actions = new_restful_apis('第三方API接入申请', '/api/tickets/vendor_api_applies/', VendorApiApplyViewSet)
doc.add_apis(api2, api3, *actions)

api1, api2, api3, actions = new_restful_apis('产品上线申请', '/api/tickets/product_launch_applies/', ProductLaunchApplyViewSet)
doc.add_apis(api2, api3, *actions)

api1, api2, api3, actions = new_restful_apis('工单', '/api/tickets/tickets/', TicketViewSet)
doc.add_apis(api1, api3, *actions)

doc.build('api.html', 'zh')
