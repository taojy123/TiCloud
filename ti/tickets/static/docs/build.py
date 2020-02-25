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
    QP(name='user_department', description='指定用户部门'),
    QP(name='creator', description='指定创建人'),
    QP(name='org_name_zh', description='匹配机构中文名称'),
    QP(name='org_name_en', description='匹配机构英文名称'),
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
            "description": ""
        }
    ]
}
"""
doc.apis.append(api3)


api4 = api2.clone()
api4.title = '创建用户测试申请'
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
    "description": ""
}
"""
doc.apis.append(api4)


doc.build('api.html', 'zh')

