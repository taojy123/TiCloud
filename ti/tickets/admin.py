from django.contrib import admin

from tickets import models


@admin.register(models.ConsumerLaunchApply)
class ConsumerLaunchApplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'oa_number', 'category', 'org_name_zh', 'org_name_en']


@admin.register(models.ConsumerTrialApply)
class ConsumerTrialApplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'oa_number', 'category', 'org_name_zh', 'org_name_en']


@admin.register(models.ProductLaunchApply)
class ProductLaunchApplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_number', 'product_name', 'source_numbers']


@admin.register(models.VendorApply)
class VendorApplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'org_code', 'org_name_zh', 'org_number']


@admin.register(models.VendorApiApply)
class VendorApiApplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'org_code', 'product_name', 'api_code', 'product_description']

