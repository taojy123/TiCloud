from django.contrib import admin
from django.contrib.auth.models import Group

from tickets import models


class ModelAdmin(admin.ModelAdmin):

    list_per_page = 50
    list_max_show_all = 5000
    list_display = []

    def lookup_allowed(self, lookup, value):
        return True

    def __init__(self, model, admin_site):
        if not self.list_display:
            self.list_display = [field.name for field in model._meta.fields]
        super().__init__(model, admin_site)


@admin.register(models.User)
class UserAdmin(ModelAdmin):
    list_display = ['id', 'username', 'password', 'email', 'full_name', 'mobile', 'department', 'job', 'leader']
    list_filter = ['department']
    search_fields = ['username', 'full_name']
    fields = ['username', 'password', 'email', 'full_name', 'mobile', 'department', 'job', 'leader', 'is_active', 'is_staff', 'is_superuser']
    raw_id_fields = ['leader']

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


@admin.register(models.ConsumerRegisterApply)
class ConsumerRegisterApplyAdmin(ModelAdmin):
    list_display = ['id', 'name', 'username', 'category', 'org_name_zh', 'org_name_en']


@admin.register(models.ConsumerOrderApply)
class ConsumerOrderApplyAdmin(ModelAdmin):
    list_display = ['id', 'username', 'contract_status', 'user_department', 'user_project', 'user_product', 'related_products']


@admin.register(models.ConsumerTrialApply)
class ConsumerTrialApplyAdmin(ModelAdmin):
    list_display = ['id', 'username', 'user_department', 'user_project', 'user_product', 'related_products']


@admin.register(models.VendorApply)
class VendorApplyAdmin(ModelAdmin):
    list_display = ['id', 'org_code', 'org_name_zh', 'org_number']


@admin.register(models.VendorApiApply)
class VendorApiApplyAdmin(ModelAdmin):
    list_display = ['id', 'org_code', 'product_name', 'api_code', 'product_description']


@admin.register(models.ProductLaunchApply)
class ProductLaunchApplyAdmin(ModelAdmin):
    list_display = ['id', 'product_number', 'product_name', 'source_numbers']


@admin.register(models.Ticket)
class TicketAdmin(ModelAdmin):
    raw_id_fields = ['applicant', 'maintainer', 'creator']


@admin.register(models.TicketFlow)
class TicketFlowAdmin(ModelAdmin):
    raw_id_fields = ['ticket']


@admin.register(models.Attachment)
class AttachmentAdmin(ModelAdmin):
    raw_id_fields = ['ticket']
    list_display = ['id', 'ticket', 'name']


admin.site.unregister(Group)

