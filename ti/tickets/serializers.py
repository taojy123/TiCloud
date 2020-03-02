import random
import uuid

from rest_framework import serializers, exceptions

from tickets.models import ConsumerTrialApply, ConsumerLaunchApply, VendorApply, VendorApiApply, ProductLaunchApply, \
    Ticket, TicketFlow


class TicketFlowSerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketFlow
        fields = '__all__'
        read_only_fields = ['updated_at']
        depth = 0


class TicketSerializer(serializers.ModelSerializer):

    flows = TicketFlowSerializer(many=True, read_only=True)
    apply_uri = serializers.CharField(read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['relate_code', 'status', 'created_at']


class ApplySerializer(serializers.ModelSerializer):
    
    ticket = TicketSerializer(read_only=True)
    title = serializers.CharField(write_only=True, required=True, label='工单任务主题')
    applicant = serializers.CharField(write_only=True, required=False, label='工单申请人', help_text='可以代别人申请')
    applicant_department = serializers.CharField(write_only=True, required=False, label='工单申请人部门')
    applicant_job = serializers.CharField(write_only=True, required=False, label='工单申请人职位')
    
    def create(self, validated_data):
        title = validated_data.pop('title')
        applicant = validated_data.pop('applicant', '')
        applicant_department = validated_data.pop('applicant_department', '')
        applicant_job = validated_data.pop('applicant_job', '')
        instance = super().create(validated_data)
        relate_code = f'{instance.__class__.__name__}_{instance.id}'
        ticket = Ticket()
        ticket.number = uuid.uuid4().hex
        ticket.relate_code = relate_code
        ticket.title = title
        ticket.applicant = applicant
        ticket.applicant_department = applicant_department
        ticket.applicant_job = applicant_job
        ticket.status = '未提交'
        ticket.save()
        return instance


class ConsumerTrialApplySerializer(ApplySerializer):
    
    def create(self, validated_data):
        instance = super().create(validated_data)
        ticket = instance.ticket
        assert ticket
        ticket.ticketflow_set.create(
            sequence=1,
            handler_name='test',
        )
        ticket.ticketflow_set.create(
            sequence=2,
            handler_name='test2',
        )
        return instance
    
    class Meta:
        model = ConsumerTrialApply
        fields = '__all__'


class ConsumerLaunchApplySerializer(ApplySerializer):
    
    class Meta:
        model = ConsumerLaunchApply
        fields = '__all__'


class VendorApplySerializer(ApplySerializer):
    
    class Meta:
        model = VendorApply
        fields = '__all__'


class VendorApiApplySerializer(ApplySerializer):
    
    class Meta:
        model = VendorApiApply
        fields = '__all__'


class ProductLaunchApplySerializer(ApplySerializer):
    
    class Meta:
        model = ProductLaunchApply
        fields = '__all__'

