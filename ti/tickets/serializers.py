import random
from rest_framework import serializers, exceptions

from tickets.models import ConsumerTrialApply, ConsumerLaunchApply, VendorApply, VendorApiApply, ProductLaunchApply


class ConsumerTrialApplySerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsumerTrialApply
        fields = ['id', 'username', 'oa_number', 'category', 'org_name_zh', 'org_name_en', 'org_number', 'org_address',
                  'user_department', 'user_project', 'user_product', 'test_count', 'server_ips', 'contact_person',
                  'contact_mobile', 'contact_email', 'related_products', 'creator', 'creator_mobile', 'creator_email',
                  'description']


class ConsumerLaunchApplySerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsumerLaunchApply
        fields = ['id', 'username', 'oa_number', 'category', 'org_name_zh', 'org_name_en', 'org_number', 'org_address',
                  'user_department', 'user_project', 'user_product', 'server_ips', 'contact_person', 'contact_mobile',
                  'contact_email', 'related_products', 'creator', 'creator_mobile', 'creator_email', 'description']


class VendorApplySerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorApply
        fields = ['id', 'org_code', 'org_name_zh', 'org_number', 'contact_person', 'contact_mobile', 'contact_email',
                  'org_address', 'creator', 'creator_mobile', 'creator_email', 'score', 'risk', 'communication',
                  'industry', 'description']


class VendorApiApplySerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorApiApply
        fields = ['id', 'org_code', 'product_name', 'api_code', 'product_description', 'api_url', 'params_in',
                  'params_in_sensitive', 'params_out_sensitive', 'use_cache', 'cache_ms', 'timeout_ms', 'field',
                  'alarm_total_count', 'alarm_fail_count', 'alarm_timeout_count', 'start', 'send', 'version', 'remark']


class ProductLaunchApplySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductLaunchApply
        fields = ['id', 'product_number', 'product_name', 'source_numbers', 'manager_name', 'manager_mobile',
                  'manager_email', 'use_cache', 'cache_ms', 'timeout_ms', 'alarm_total_count', 'alarm_fail_count',
                  'alarm_timeout_count', 'params_in', 'params_in_sensitive', 'params_out_sensitive', 'creator',
                  'creator_mobile', 'creator_email', 'creator_department', 'remark']


