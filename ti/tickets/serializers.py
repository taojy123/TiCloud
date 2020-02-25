import random
from rest_framework import serializers, exceptions

from tickets.models import ConsumerTrialApply, ConsumerLaunchApply


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


