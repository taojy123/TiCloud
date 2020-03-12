import os

from eave import *
from eave.utils import auto_drf_apis

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ti.settings")
import django
django.setup()

from tickets.views import ProductLaunchApplyViewSet, ConsumerTrialApplyViewSet, VendorApplyViewSet, \
    VendorApiApplyViewSet, TicketViewSet, UserViewSet, ConsumerRegisterApplyViewSet, ConsumerOrderApplyViewSet


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


api1, api2, api3, actions = auto_drf_apis('系统用户', '/api/tickets/users/', UserViewSet)
doc.add_apis(api1, *actions)

api1, api2, api3, actions = auto_drf_apis('用户注册申请', '/api/tickets/consumer_register_applies/', ConsumerRegisterApplyViewSet)
doc.add_apis(api2, api3, *actions)

api1, api2, api3, actions = auto_drf_apis('用户订单申请', '/api/tickets/consumer_order_applies/', ConsumerOrderApplyViewSet)
doc.add_apis(api2, api3, *actions)

api1, api2, api3, actions = auto_drf_apis('用户测试申请', '/api/tickets/consumer_trial_applies/', ConsumerTrialApplyViewSet)
doc.add_apis(api2, api3, *actions)

api1, api2, api3, actions = auto_drf_apis('第三方供应商注册申请', '/api/tickets/vendor_applies/', VendorApplyViewSet)
doc.add_apis(api2, api3, *actions)

api1, api2, api3, actions = auto_drf_apis('第三方API接入申请', '/api/tickets/vendor_api_applies/', VendorApiApplyViewSet)
doc.add_apis(api2, api3, *actions)

api1, api2, api3, actions = auto_drf_apis('产品上线申请', '/api/tickets/product_launch_applies/', ProductLaunchApplyViewSet)
doc.add_apis(api2, api3, *actions)

api1, api2, api3, actions = auto_drf_apis('工单', '/api/tickets/tickets/', TicketViewSet)
doc.add_apis(api1, api3, *actions)

doc.build('tickets.html', 'zh')
