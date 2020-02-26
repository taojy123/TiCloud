from eave import *

doc = Doc(
    title='工单系统接口文档',
    version='1.0.0',
    host='http://172.23.43.15:8882',
    description='',
)

api1 = Api()
api1.title = '用户测试申请列表'
api1.uri = '/api/tickets/consumer_trial_apply/'
api1.method = 'GET'
api1.query_params = [
    QP(name='creator', description='指定创建人'),
    QP(name='creator_department', description='指定用户部门'),
    QP(name='org_name_zh__icontains', description='匹配机构中文名称'),
    QP(name='org_name_en__icontains', description='匹配机构英文名称'),
    QP(name='org_number', description='指定社会统一信用代码/组织机构代码'),
]
api1.response_example = r"""
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "username": "test111",
            "oa_number": "test2222",
            "category": 1,
            "org_name_zh": "测测次",
            "org_name_en": "test",
            "org_number": "1234567890987654",
            "org_address": "xxxxx",
            "user_department": "testdepartment",
            "user_project": "testproj",
            "user_product": "testprod",
            "test_count": 97,
            "server_ips": "",
            "contact_person": "张三",
            "contact_mobile": "13412345678",
            "contact_email": "ta@admin.com",
            "related_products": "fss,fff,s333",
            "creator": "ff",
            "creator_mobile": "13402110752",
            "creator_email": "22@44.com",
            "creator_department": "testdepartment",
            "description": "afjasjf\r\nasdflkas\r\n\r\n\r\nasfsf"
        }
    ]
}
"""
doc.apis.append(api1)


api2 = api1.clone()
api2.title = '创建用户测试申请'
api2.method = 'POST'
api2.query_params = []
api2.body_params = [
    BP(name='username', description='用户账号(唯一标识对该用户授权访问的一个访问通道编码。编码规则：机构中文全拼缩写（小写 ）+ 4位16进制随机编码，由业务输入系统 （系统应具备验证用户名唯一性功能）。用户账号由业务生成，生成的过程中，能够校验账号的唯一性)', required=True),
    BP(name='oa_number', description='协议OA审批编号(用户申请测试，如果测试连接第三方生产环境，有费用发生，需要走OA流程，知会财务；如果是自己数据源，小宇100条免费，可以不用走OA，大于100条需要走OA流程审批)', required=False),
    BP(name='category', type='int', description='用户类型(1 内部用户； 2 外部用户)', required=True),
    BP(name='org_name_zh', description='机构中文名称(可以为空，但是中英文单位名称必须填一个)', required=False),
    BP(name='org_name_en', description='机构英文名称(可以为空，但是中英文单位名称必须填一个)', required=False),
    BP(name='org_number', description='社会统一信用代码/组织机构代码 (用于客户业务校核，客户的中英文名称应该与社会统一信用代码一致)', required=True),
    BP(name='org_address', description='机构地址(可以为空)', required=False),
    BP(name='user_department', description='用户部门(主要是配置必要的辅助信息，用于对账，内部用户必填)', required=False),
    BP(name='user_project', description='用户项目(内部用户必填)', required=False),
    BP(name='user_product', description='用户产品(内部用户必填)', required=False),
    BP(name='test_count', type='int', description='测试条数(默认测试100条)', required=True),
    BP(name='server_ips', description='服务器IP(用于配置白名单，多个IP以逗号分隔)', required=False),
    BP(name='contact_person', description='联系人(必填)', required=True),
    BP(name='contact_mobile', description='联系人手机号码(必填)', required=True),
    BP(name='contact_email', description='联系人邮箱(必填)', required=True),
    BP(name='related_products', description='用户关联产品(多个产品以逗号分隔)', required=False),
    BP(name='creator', description='创建人(必填)', required=True),
    BP(name='creator_mobile', description='创建人手机号码(必填)', required=True),
    BP(name='creator_email', description='创建人邮箱(必填)', required=True),
    BP(name='creator_department', description='创建人部门(必填)', required=True),
    BP(name='description', description='描述(可以描述附加的客户需求)', required=False),
]
api2.response_example = r"""
{
    "id": 1,
    "username": "test111",
    "oa_number": "test2222",
    "category": 1,
    "org_name_zh": "测测次",
    "org_name_en": "test",
    "org_number": "1234567890987654",
    "org_address": "xxxxxx",
    "user_department": "testdepartment",
    "user_project": "testproj",
    "user_product": "testprod",
    "test_count": 97,
    "server_ips": "",
    "contact_person": "张三",
    "contact_mobile": "13412345678",
    "contact_email": "ta@admin.com",
    "related_products": "fss,fff,s333",
    "creator": "ff",
    "creator_mobile": "13402110752",
    "creator_email": "22@44.com",
    "creator_department": "testdepartment",
    "description": "afjasjf\r\nasdflkas\r\n\r\n\r\nasfsf"
}
"""
doc.apis.append(api2)


api3 = api1.clone()
api3.title = '用户上线申请列表'
api3.uri = '/api/tickets/consumer_launch_apply/'
api3.response_example = r"""
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "username": "test11",
            "oa_number": "xxx",
            "category": 2,
            "org_name_zh": "测测次",
            "org_name_en": "test",
            "org_number": "1234567890987654",
            "org_address": "",
            "user_department": "testdepartment",
            "user_project": "testproj",
            "user_product": "testprod",
            "server_ips": "",
            "contact_person": "张三",
            "contact_mobile": "13402110752",
            "contact_email": "ta@admin.com",
            "related_products": "",
            "creator": "ff",
            "creator_mobile": "134012342212",
            "creator_email": "22@44.com",
            "creator_department": "testdepartment",
            "description": ""
        }
    ]
}
"""
doc.apis.append(api3)


api4 = api2.clone()
api4.title = '创建用户上线申请'
api4.uri = '/api/tickets/consumer_launch_apply/'
api4.body_params = [
    BP(name='username', description='用户账号(唯一标识对该用户授权访问的一个访问通道编码。编码规则：机构中文全拼缩写（小写 ）+ 4位16进制随机编码，由业务输入系统 （系统应具备验证用户名唯一性功能）。用户账号由业务生成，生成的过程中，能够校验账号的唯一性)', required=True),
    BP(name='oa_number', description='用户申请使用生产系统的产品，需要先签订合同，并OA审批通过', required=False),
    BP(name='category', type='int', description='用户类型(1 内部用户； 2 外部用户)', required=True),
    BP(name='org_name_zh', description='机构中文名称(可以为空，但是中英文单位名称必须填一个)', required=False),
    BP(name='org_name_en', description='机构英文名称(可以为空，但是中英文单位名称必须填一个)', required=False),
    BP(name='org_number', description='社会统一信用代码/组织机构代码 (用于客户业务校核，客户的中英文名称应该与社会统一信用代码一致)', required=True),
    BP(name='org_address', description='机构地址(可以为空)', required=False),
    BP(name='user_department', description='用户部门(主要是配置必要的辅助信息，用于对账，内部用户必填)', required=False),
    BP(name='user_project', description='用户项目(内部用户必填)', required=False),
    BP(name='user_product', description='用户产品(内部用户必填)', required=False),
    BP(name='server_ips', description='服务器IP(用于配置白名单，多个IP以逗号分隔)', required=False),
    BP(name='contact_person', description='联系人(必填)', required=True),
    BP(name='contact_mobile', description='联系人手机号码(必填)', required=True),
    BP(name='contact_email', description='联系人邮箱(必填)', required=True),
    BP(name='related_products', description='用户关联产品(多个产品以逗号分隔)', required=False),
    BP(name='creator', description='创建人(必填)', required=True),
    BP(name='creator_mobile', description='创建人手机号码(必填)', required=True),
    BP(name='creator_email', description='创建人邮箱(必填)', required=True),
    BP(name='creator_department', description='创建人部门(必填)', required=True),
    BP(name='description', description='描述(可以描述附加的客户需求)', required=False),
]
api4.response_example = r"""
{
    "id": 2,
    "username": "test112",
    "oa_number": "xxx",
    "category": 2,
    "org_name_zh": "测测次",
    "org_name_en": "test",
    "org_number": "1234567890987654",
    "org_address": "",
    "user_department": "testdepartment",
    "user_project": "testproj",
    "user_product": "testprod",
    "server_ips": "",
    "contact_person": "张三",
    "contact_mobile": "13402110752",
    "contact_email": "ta@admin.com",
    "related_products": "",
    "creator": "ff",
    "creator_mobile": "134012342212",
    "creator_email": "22@44.com",
    "creator_department": "testdepartment",
    "description": ""
}
"""
doc.apis.append(api4)


api5 = api1.clone()
api5.title = '第三方供应商注册申请列表'
api5.uri = '/api/tickets/vendor_apply/'
api5.query_params = [
    QP(name='creator', description='指定创建人'),
    QP(name='creator_department', description='指定用户部门'),
    QP(name='org_name_zh__icontains', description='匹配机构中文名称'),
    QP(name='org_code__icontains', description='匹配机构编码'),
]
api5.response_example = r"""
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "org_code": "test1123",
            "org_name_zh": "测测次",
            "org_number": "1234567890987654",
            "contact_person": "张三",
            "contact_mobile": "13402110752",
            "contact_email": "",
            "org_address": "xxxx",
            "creator": "ff",
            "creator_mobile": "13402110752",
            "creator_email": "22@44.com",
            "score": 2,
            "risk": 3,
            "communication": "",
            "industry": "xxx",
            "description": ""
        }
    ]
}
"""
doc.apis.append(api5)


api6 = api2.clone()
api6.title = '创建第三方供应商注册申请'
api6.uri = '/api/tickets/vendor_apply/'
api6.body_params = [
    BP(name='org_code', description='机构编码(供应商的唯一标识。编码规则：机构中文全拼缩写（小写 ）+ 4位16进制随机编码，由业务输入系统 （系统应具备验证用户名唯一性功能）。用户账号由业务生成，生成的过程中，能够校验账号的唯一性。该账号也是供应商访问日志的登录账号)', required=True),
    BP(name='org_name_zh', description='机构中文名称(如：白骑士，机构名称全局唯一，如果系统有多个相同名称，应该以序号自动区分。)', required=True),
    BP(name='org_number', description='机构社会统一信用编码(必须，用于客户业务校核，客户的中文名称应该与社会统一信用代码一致 )', required=True),
    BP(name='contact_person', description='联系人(必填)', required=True),
    BP(name='contact_mobile', description='联系人手机号码(必填)', required=True),
    BP(name='contact_email', description='联系人邮箱(必填)', required=True),
    BP(name='org_address', description='机构地址(可以为空)', required=False),
    BP(name='creator', description='创建人(必填)', required=True),
    BP(name='creator_mobile', description='创建人手机号码(必填)', required=True),
    BP(name='creator_email', description='创建人邮箱(必填)', required=True),
    BP(name='creator_department', description='创建人部门(必填)', required=True),
    BP(name='score', type='int', description='评分(评分分为1~5分，最开始进入系统都为0分)', required=True),
    BP(name='risk', type='int', description='风险(风险分为1~5级，最开始进入系统都为0级，没有风险)', required=True),
    BP(name='communication', description='沟通记录(与供应商沟通后，特别需要关注的问题)', required=False),
    BP(name='industry', description='所属行业(必填)', required=True),
    BP(name='description', description='描述(可以描述附加的客户需求)', required=False),
]
api6.response_example = r"""
{
    "id": 1,
    "org_code": "test1123",
    "org_name_zh": "测测次",
    "org_number": "1234567890987654",
    "contact_person": "张三",
    "contact_mobile": "13402110752",
    "contact_email": "",
    "org_address": "xxxx",
    "creator": "ff",
    "creator_mobile": "13402110752",
    "creator_email": "22@44.com",
    "score": 2,
    "risk": 3,
    "communication": "",
    "industry": "xxx",
    "description": ""
}
"""
doc.apis.append(api6)


api7 = api1.clone()
api7.title = '第三方API接入申请列表'
api7.uri = '/api/tickets/vendor_api_apply/'
api7.query_params = [
    QP(name='creator', description='指定创建人'),
    QP(name='creator_department', description='指定用户部门'),
]
api7.response_example = r"""
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "org_code": "test1123",
            "product_name": "xfafsf",
            "api_code": "s33fffss",
            "product_description": "ffxxxx",
            "api_url": "https://xxx.com/api/shopex/webhooks/",
            "params_in": "",
            "params_in_sensitive": "",
            "params_out_sensitive": "",
            "use_cache": true,
            "cache_ms": 122,
            "timeout_ms": 333,
            "field": "",
            "alarm_total_count": 0,
            "alarm_fail_count": 0,
            "alarm_timeout_count": 0,
            "start": "",
            "send": "",
            "version": "",
            "remark": ""
        }
    ]
}
"""
doc.apis.append(api7)


api8 = api2.clone()
api8.title = '创建第三方API接入申请'
api8.uri = '/api/tickets/vendor_api_apply/'
api8.body_params = [
    BP(name='org_code', description='机构账编码(供应商的唯一标识。编码规则：机构中文全拼缩写（小写 ）+ 4位16进制随机编码，由业务输入系统 （系统应具备验证用户名唯一性功能）。用户账号由业务生成，生成的过程中，能够校验账号的唯一性。该账号也是供应商访问日志的登录账号)', required=True),
    BP(name='product_name', description='产品名称(必填)', required=True),
    BP(name='api_code', description='API编码(必填，满足数据源编码规范，参考《数据产品编码规范》)', required=True),
    BP(name='product_description', description='产品定义(必填，产品描述)', required=True),
    BP(name='api_url', description='API访问URL(必填)', required=True),
    BP(name='params_in', description='入参(必填)', required=True),
    BP(name='params_in_sensitive', description='入参敏感字段(必填)', required=True),
    BP(name='params_out_sensitive', description='出参敏感字段(必填)', required=True),
    BP(name='use_cache', type='bool', description='是否缓存(必填，是否使用缓存热数据返回用户)', required=True),
    BP(name='cache_ms', type='int', description='缓存时间/毫秒(必填)', required=True),
    BP(name='timeout_ms', type='int', description='超时时间/毫秒(必填)', required=True),
    BP(name='field', description='使用领域(必填)', required=True),
    BP(name='alarm_total_count', type='int', description='报警总观测次数(必填，报警累计次数)', required=True),
    BP(name='alarm_fail_count', type='int', description='失败数报警阀值(必填，失败几次开始报警)', required=True),
    BP(name='alarm_timeout_count', type='int', description='超时报警阀值(必填)', required=True),
    BP(name='start', description='开始时间(API合同生效时间)', required=False),
    BP(name='send', description='结束时间(API合同结束时间)', required=False),
    BP(name='version', description='版本号(必填，API目前注册版本号)', required=True),
    BP(name='creator', description='创建人(必填)', required=True),
    BP(name='creator_mobile', description='创建人手机号码(必填)', required=True),
    BP(name='creator_email', description='创建人邮箱(必填)', required=True),
    BP(name='creator_department', description='创建人部门(必填)', required=True),
    BP(name='remark', description='备注(可以为空，补充信息)', required=False),
]
api8.response_example = r"""
{
    "id": 1,
    "org_code": "test1123",
    "product_name": "xfafsf",
    "api_code": "s33fffss",
    "product_description": "ffxxxx",
    "api_url": "https://xxx.com/api/shopex/webhooks/",
    "params_in": "",
    "params_in_sensitive": "",
    "params_out_sensitive": "",
    "use_cache": true,
    "cache_ms": 122,
    "timeout_ms": 333,
    "field": "",
    "alarm_total_count": 0,
    "alarm_fail_count": 0,
    "alarm_timeout_count": 0,
    "start": "",
    "send": "",
    "version": "",
    "remark": ""
}
"""
doc.apis.append(api8)


doc.build('api.html', 'zh')

