from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    include：
        username、password、email、is_active、is_staff、is_superuser
    """

    full_name = models.CharField(max_length=32, blank=True, verbose_name='姓名')
    mobile = models.CharField(max_length=32, blank=True, verbose_name='手机')
    department = models.CharField(max_length=32, blank=True, verbose_name='部门')
    job = models.CharField(max_length=32, blank=True, verbose_name='职位')
    leader = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='上级主管')

    class Meta:
        verbose_name = verbose_name_plural = '用户'
        swappable = 'AUTH_USER_MODEL'


class Ticket(models.Model):
    number = models.CharField(max_length=128, blank=True, unique=True, verbose_name='工单号', help_text='唯一标识')
    relate_code = models.CharField(max_length=128, blank=True, verbose_name='关联代码', help_text='系统自动生成，用于绑定申请记录')
    title = models.CharField(max_length=128, blank=True, verbose_name='任务主题')
    applicant = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='applicant_ticket_set', verbose_name='申请人')
    maintainer = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='maintainer_ticket_set', verbose_name='维护人(责任人)')
    current_reviewer = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='reviewer_ticket_set', verbose_name='当前审批人')
    creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='creator_ticket_set', verbose_name='真实创建者')
    status = models.CharField(max_length=32, blank=True, verbose_name='工单状态', help_text='审批中/审批通过/驳回/撤回/已生效/归档')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '工单'

    def __str__(self):
        return self.title

    @property
    def flows(self):
        return self.ticketflow_set.order_by('sequence')
    
    @property
    def current_flow(self):
        # 只有再审批中的才会继续往下审批
        if self.status != '审批中':
            return None
        return self.ticketflow_set.filter(result='').order_by('sequence').first()

    @property
    def apply(self):
        if '_' not in self.relate_code:
            return
        model_name, apply_id = self.relate_code.split('_')
        ModelClass = apps.get_model('tickets', model_name)
        return ModelClass.objects.filter(id=apply_id).first()
    
    @property
    def apply_uri(self):
        if not self.apply:
            return
        model_name, apply_id = self.relate_code.split('_')
        res_name = ''
        for char in model_name:
            if char.isupper():
                char = '_' + char
            res_name += char
        res_name = res_name.lower().strip('_')
        return f'/api/tickets/{res_name}/{apply_id}/'
    
    @property
    def attachments(self):
        return self.attachment_set.all()
    

class TicketFlow(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='工单')
    sequence = models.IntegerField(default=0, verbose_name='流程次序')
    reviewer = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='审批人')
    result = models.CharField(max_length=32, blank=True, verbose_name='审批结果', help_text='同意/驳回')
    content = models.TextField(blank=True, verbose_name='审批意见')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = verbose_name_plural = '工单审批记录'
        
    def __str__(self):
        return f'{self.ticket.title}_#{self.sequence}'


class Attachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='工单')
    name = models.CharField(max_length=64, blank=True, verbose_name='名称')
    content = models.BinaryField(default=0, verbose_name='文件内容')

    class Meta:
        verbose_name = verbose_name_plural = '附件'
        
    def __str__(self):
        return self.name


# =========== applies ==============

class AbstractApply(models.Model):
    
    relate_code = models.CharField(max_length=128, blank=True, verbose_name='关联代码', help_text='系统自动生成，用于绑定工单')
    
    @property
    def ticket(self):
        relate_code = self.relate_code or f'{self.__class__.__name__}_{self.id}'
        return Ticket.objects.filter(relate_code=relate_code).first()
    
    @classmethod
    def enabled_objects(cls):
        disabled_tickets = Ticket.objects.filter(status__in=['驳回', '撤回'])
        disabled_relate_codes = disabled_tickets.values_list('relate_code', flat=True)
        return cls.objects.exclude(relate_code__in=disabled_relate_codes)
    
    class Meta:
        abstract = True


class ConsumerRegisterApply(AbstractApply):
    name = models.CharField(max_length=64, blank=True, verbose_name='用户名称', help_text='一般是中文')
    username = models.CharField(max_length=64, blank=True, verbose_name='用户账号',
                                help_text='唯一标识对该用户授权访问的一个访问通道编码。编码规则：机构中文全拼缩写（小写 ）+ 4位16进制随机编码，由业务输入系统 （系统应具备验证用户名唯一性功能）。用户账号由业务生成，生成的过程中，能够校验账号的唯一性')
    category = models.IntegerField(default=0, verbose_name='用户类型', help_text='1 内部用户； 2 外部用户')
    org_name_zh = models.CharField(max_length=256, blank=True, verbose_name='机构中文名称', help_text='必填')
    org_name_en = models.CharField(max_length=256, blank=True, verbose_name='机构英文名称', help_text='可以为空')
    org_number = models.CharField(max_length=128, blank=True, verbose_name='社会统一信用代码/组织机构代码',
                                  help_text='必填，用于客户业务校核，客户的中英文名称应该与社会统一信用代码一致')
    org_address = models.CharField(max_length=256, blank=True, verbose_name='机构地址', help_text='可以为空')
    server_ips = models.CharField(max_length=128, blank=True, verbose_name='服务器IP', help_text='用于配置白名单，多个IP以逗号分隔')
    contact_person = models.CharField(max_length=64, blank=True, verbose_name='联系人', help_text='必填')
    contact_mobile = models.CharField(max_length=64, blank=True, verbose_name='联系人手机', help_text='必填')
    contact_email = models.CharField(max_length=64, blank=True, verbose_name='联系人邮箱', help_text='必填')
    score = models.IntegerField(default=0, verbose_name='评分', help_text='评分分为1~5分，最开始进入系统都为0分')
    risk = models.IntegerField(default=0, verbose_name='风险', help_text='风险分为1~5级，最开始进入系统都为0级，没有风险')
    communication = models.TextField(blank=True, verbose_name='沟通记录', help_text='与供应商沟通后，特别需要关注的问题')
    industry = models.CharField(max_length=64, blank=True, verbose_name='所属行业', help_text='必填')
    description = models.TextField(blank=True, verbose_name='描述', help_text='可以描述附加的需求')
    
    class Meta:
        verbose_name = verbose_name_plural = '用户注册申请'
    
    def __str__(self):
        return self.username


class ConsumerOrderApply(AbstractApply):
    username = models.CharField(max_length=64, blank=True, verbose_name='用户账号', help_text='唯一标识')
    oa_number = models.CharField(max_length=128, blank=True, verbose_name='协议OA审批编号',
                                 help_text='用户申请使用生产系统的产品，需要先签订合同，并OA审批通过')
    contract_status = models.CharField(max_length=32, blank=True, verbose_name='合同状态', help_text='审批通过，才能申请订单')
    user_department = models.CharField(max_length=128, blank=True, verbose_name='用户部门',
                                       help_text='主要是配置必要的辅助信息，用于对账，内部用户必填')
    user_project = models.CharField(max_length=128, blank=True, verbose_name='用户项目', help_text='内部用户必填')
    user_product = models.CharField(max_length=128, blank=True, verbose_name='用户产品', help_text='内部用户必填')
    related_products = models.CharField(max_length=256, blank=True, verbose_name='用户关联产品编码', help_text='多个产品以逗号分隔')
    test_count = models.IntegerField(default=5, verbose_name='生产接入测试条数', help_text='默认5条')
    description = models.TextField(blank=True, verbose_name='描述', help_text='可以描述附加的需求')
    
    class Meta:
        verbose_name = verbose_name_plural = '用户订单申请'
    
    def __str__(self):
        return self.username


class ConsumerTrialApply(AbstractApply):
    username = models.CharField(max_length=64, blank=True, verbose_name='用户账号',
                                help_text='唯一标识对该用户授权访问的一个访问通道编码。编码规则：机构中文全拼缩写（小写 ）+ 4位16进制随机编码，由业务输入系统 （系统应具备验证用户名唯一性功能）。用户账号由业务生成，生成的过程中，能够校验账号的唯一性')
    oa_number = models.CharField(max_length=128, blank=True, verbose_name='协议OA审批编号', help_text='可以为空')
    user_department = models.CharField(max_length=128, blank=True, verbose_name='用户部门',
                                       help_text='主要是配置必要的辅助信息，用于对账，内部用户必填')
    user_project = models.CharField(max_length=128, blank=True, verbose_name='用户项目', help_text='内部用户必填')
    user_product = models.CharField(max_length=128, blank=True, verbose_name='用户产品', help_text='内部用户必填')
    test_count = models.IntegerField(default=100, verbose_name='测试条数', help_text='默认测试100条')
    related_products = models.CharField(max_length=256, blank=True, verbose_name='用户关联产品编码', help_text='多个产品以逗号分隔')
    description = models.TextField(blank=True, verbose_name='描述', help_text='可以描述附加的需求')
    
    class Meta:
        verbose_name = verbose_name_plural = '用户测试申请'
    
    def __str__(self):
        return self.username


class VendorApply(AbstractApply):
    org_code = models.CharField(max_length=64, blank=True, verbose_name='机构编码',
                                help_text='供应商的唯一标识。编码规则：机构中文全拼缩写（小写 ）+ 4位16进制随机编码，由业务输入系统 （系统应具备验证用户名唯一性功能）。用户账号由业务生成，生成的过程中，能够校验账号的唯一性。该账号也是供应商访问日志的登录账号')
    org_name_zh = models.CharField(max_length=64, blank=True, verbose_name='机构中文名称',
                                   help_text='如：白骑士，机构名称全局唯一，如果系统有多个相同名称，应该以序号自动区分。')
    org_number = models.CharField(max_length=64, blank=True, verbose_name='机构社会统一信用编码',
                                  help_text='必须，用于客户业务校核，客户的中文名称应该与社会统一信用代码一致 ')
    contact_person = models.CharField(max_length=64, blank=True, verbose_name='联系人', help_text='必填')
    contact_mobile = models.CharField(max_length=64, blank=True, verbose_name='联系人手机号码', help_text='必填')
    contact_email = models.CharField(max_length=64, blank=True, verbose_name='联系人邮箱', help_text='必填')
    org_address = models.CharField(max_length=256, blank=True, verbose_name='机构地址', help_text='可以为空')
    score = models.IntegerField(default=0, verbose_name='评分', help_text='评分分为1~5分，最开始进入系统都为0分')
    risk = models.IntegerField(default=0, verbose_name='风险', help_text='风险分为1~5级，最开始进入系统都为0级，没有风险')
    communication = models.TextField(blank=True, verbose_name='沟通记录', help_text='与供应商沟通后，特别需要关注的问题')
    industry = models.CharField(max_length=64, blank=True, verbose_name='所属行业', help_text='必填')
    description = models.TextField(blank=True, verbose_name='描述', help_text='可以描述附加的需求')
    
    class Meta:
        verbose_name = verbose_name_plural = '第三方供应商注册申请'
    
    def __str__(self):
        return self.org_code


class VendorApiApply(AbstractApply):
    org_code = models.CharField(max_length=64, blank=True, verbose_name='机构编码',
                                help_text='供应商的唯一标识。编码规则：机构中文全拼缩写（小写 ）+ 4位16进制随机编码，由业务输入系统 （系统应具备验证用户名唯一性功能）。用户账号由业务生成，生成的过程中，能够校验账号的唯一性。该账号也是供应商访问日志的登录账号')
    product_name = models.CharField(max_length=64, blank=True, verbose_name='产品名称', help_text='必填')
    api_code = models.CharField(max_length=64, blank=True, verbose_name='API编码', help_text='必填，满足数据源编码规范，参考《数据产品编码规范》')
    product_description = models.CharField(max_length=64, blank=True, verbose_name='产品定义', help_text='必填，产品描述')
    api_url = models.CharField(max_length=64, blank=True, verbose_name='API访问URL', help_text='必填')
    params_in = models.TextField(blank=True, default='{}', verbose_name='入参', help_text='必填，json 结构体')
    params_in_sensitive = models.TextField(blank=True, verbose_name='入参敏感字段', help_text='必填，多个字段用逗号分隔')
    params_out_sensitive = models.TextField(blank=True, verbose_name='出参敏感字段', help_text='必填，多个字段用逗号分隔')
    use_cache = models.BooleanField(default=False, verbose_name='是否缓存', help_text='必填，是否使用缓存热数据返回用户')
    cache_ms = models.IntegerField(default=0, verbose_name='缓存时间/毫秒', help_text='必填')
    timeout_ms = models.IntegerField(default=0, verbose_name='超时时间/毫秒', help_text='必填')
    field = models.CharField(max_length=64, blank=True, verbose_name='使用领域', help_text='必填')
    alarm_total_count = models.IntegerField(default=0, verbose_name='报警总观测次数', help_text='必填，报警累计次数')
    alarm_fail_count = models.IntegerField(default=0, verbose_name='失败数报警阀值', help_text='必填，失败几次开始报警')
    alarm_timeout_count = models.IntegerField(default=0, verbose_name='超时报警阀值', help_text='必填')
    start = models.CharField(max_length=64, blank=True, verbose_name='开始时间', help_text='API合同生效时间')
    send = models.CharField(max_length=64, blank=True, verbose_name='结束时间', help_text='API合同结束时间')
    version = models.CharField(max_length=64, blank=True, verbose_name='版本号', help_text='必填，API目前注册版本号')
    remark = models.TextField(blank=True, verbose_name='备注', help_text='可以为空，补充信息')
    
    class Meta:
        verbose_name = verbose_name_plural = '第三方供应商API接入申请'
    
    def __str__(self):
        return self.product_name


class ProductLaunchApply(AbstractApply):
    product_number = models.CharField(max_length=64, blank=True, verbose_name='产品编号', help_text='唯一标识')
    product_name = models.CharField(max_length=128, blank=True, verbose_name='产品名称', help_text='必填')
    source_numbers = models.CharField(max_length=256, blank=True, verbose_name='数据源编码',
                                      help_text='必填，来自第三方API接入或者内部开发数据源，多个数据源以逗号分隔')
    manager_name = models.CharField(max_length=64, blank=True, verbose_name='产品经理姓名', help_text='必填')
    manager_mobile = models.CharField(max_length=64, blank=True, verbose_name='产品经理手机号码', help_text='必填')
    manager_email = models.CharField(max_length=64, blank=True, verbose_name='产品经理邮箱', help_text='必填')
    use_cache = models.BooleanField(default=False, verbose_name='是否缓存', help_text='必填，是否使用缓存热数据返回用户')
    cache_ms = models.IntegerField(default=0, verbose_name='缓存时间（毫秒）', help_text='必填')
    timeout_ms = models.IntegerField(default=0, verbose_name='超时时间（毫秒）', help_text='必填')
    alarm_total_count = models.IntegerField(default=0, verbose_name='报警总观测次数', help_text='必填，报警累计次数')
    alarm_fail_count = models.IntegerField(default=0, verbose_name='失败数报警阀值', help_text='必填，失败几次开始报警')
    alarm_timeout_count = models.IntegerField(default=0, verbose_name='超时报警阀值', help_text='必填')
    params_in = models.TextField(blank=True, default='{}', verbose_name='入参', help_text='必填')
    params_in_sensitive = models.TextField(blank=True, default='{}', verbose_name='入参敏感字段', help_text='必填')
    params_out_sensitive = models.TextField(blank=True, default='{}', verbose_name='出参敏感字段', help_text='必填')
    remark = models.TextField(blank=True, verbose_name='备注', help_text='可以为空，补充信息')
    
    class Meta:
        verbose_name = verbose_name_plural = '产品上线申请'
    
    def __str__(self):
        return self.product_name


try:
    u1 = User.objects.create(
        username='test',
        email='test@123.com',
        full_name='张三',
        mobile='13412345678',
        department='DDC',
        job='产品总监',
    )
    u1.set_password('123456')
    u1.save()
    
    u2 = User.objects.create(
        username='test2',
        email='test2@123.com',
        full_name='李四',
        mobile='13212345678',
        department='DDC',
        job='产品经理',
        leader=u1,
    )
    u2.set_password('123456')
    u2.save()
    
    u3 = User.objects.create(
        username='test3',
        email='test3@123.com',
        full_name='王五',
        mobile='13312345678',
        department='ITC',
        job='开发总监',
    )
    u3.set_password('123456')
    u3.save()
    
    u4 = User.objects.create(
        username='test4',
        email='test4@123.com',
        full_name='赵六',
        mobile='13612345678',
        department='ITC',
        job='工程师',
        leader=u3,
    )
    u4.set_password('123456')
    u4.save()
    print('user init finish')
except:
    pass


# Deprecated
# remain here for migrate
class ApplyMixin:
    pass

