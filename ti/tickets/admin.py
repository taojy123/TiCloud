from django.contrib import admin

from tickets import models


class ModelAdmin(admin.ModelAdmin):
    list_max_show_all = 10000
    list_display = []

    def __init__(self, model, admin_site):
        if not self.list_display:
            self.list_display = [field.name for field in model._meta.fields]
        super().__init__(model, admin_site)


@admin.register(models.ConsumerLaunchApply)
class ConsumerLaunchApplyAdmin(ModelAdmin):
    list_display = ['id', 'username', 'oa_number', 'category', 'org_name_zh', 'org_name_en']


@admin.register(models.ConsumerTrialApply)
class ConsumerTrialApplyAdmin(ModelAdmin):
    list_display = ['id', 'username', 'oa_number', 'category', 'org_name_zh', 'org_name_en']


@admin.register(models.ProductLaunchApply)
class ProductLaunchApplyAdmin(ModelAdmin):
    list_display = ['id', 'product_number', 'product_name', 'source_numbers']


@admin.register(models.VendorApply)
class VendorApplyAdmin(ModelAdmin):
    list_display = ['id', 'org_code', 'org_name_zh', 'org_number']


@admin.register(models.VendorApiApply)
class VendorApiApplyAdmin(ModelAdmin):
    list_display = ['id', 'org_code', 'product_name', 'api_code', 'product_description']


@admin.register(models.Ticket)
class TicketAdmin(ModelAdmin):
    pass


@admin.register(models.TicketFlow)
class TicketAdmin(ModelAdmin):
    raw_id_fields = ['ticket']


