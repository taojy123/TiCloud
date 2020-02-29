import random
from rest_framework import serializers, exceptions

from tickets.models import ConsumerTrialApply, ConsumerLaunchApply, VendorApply, VendorApiApply, ProductLaunchApply, \
    Ticket, TicketFlow


class ConsumerTrialApplySerializer(serializers.ModelSerializer):


    class Meta:
        model = ConsumerTrialApply
        fields = '__all__'


class ConsumerLaunchApplySerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsumerLaunchApply
        fields = '__all__'


class VendorApplySerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorApply
        fields = '__all__'


class VendorApiApplySerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorApiApply
        fields = '__all__'


class ProductLaunchApplySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductLaunchApply
        fields = '__all__'


class TicketFlowSerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketFlow
        fields = '__all__'
        read_only_fields = ['created_at']
        depth = 0


class TicketSerializer(serializers.ModelSerializer):

    flows = TicketFlowSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['status', 'created_at']


