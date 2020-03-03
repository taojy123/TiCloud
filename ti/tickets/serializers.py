import random
import uuid

from rest_framework import serializers, exceptions

from tickets.models import ConsumerTrialApply, VendorApply, VendorApiApply, ProductLaunchApply, \
    Ticket, TicketFlow, User, ConsumerRegisterApply, Attachment, ConsumerOrderApply


class LeaderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'mobile', 'department', 'job']


class UserSerializer(serializers.ModelSerializer):
    
    leader = LeaderSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'mobile', 'department', 'job', 'leader']
        
        
class TicketFlowSerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketFlow
        fields = '__all__'
        read_only_fields = ['updated_at']
        
        
class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attachment
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):

    flows = TicketFlowSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    apply_uri = serializers.CharField(read_only=True)
    applicant = UserSerializer(read_only=True)
    maintainer = UserSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['relate_code', 'status', 'created_at']


class ApplySerializer(serializers.ModelSerializer):
    
    ticket = TicketSerializer(read_only=True)
    title = serializers.CharField(write_only=True, label='工单任务主题')
    applicant_username = serializers.CharField(write_only=True, label='工单申请人', help_text='一般是自己')
    maintainer_username = serializers.CharField(write_only=True, label='关系维护人', help_text='可以填其他人')
    
    def create(self, validated_data):
        title = validated_data.pop('title')
        applicant_username = validated_data.pop('applicant_username')
        maintainer_username = validated_data.pop('maintainer_username')
        applicant = User.objects.filter(username=applicant_username).first()
        maintainer = User.objects.filter(username=maintainer_username).first()
        instance = super().create(validated_data)
        relate_code = f'{instance.__class__.__name__}_{instance.id}'
        ticket = Ticket()
        ticket.number = uuid.uuid4().hex
        ticket.relate_code = relate_code
        ticket.title = title
        ticket.applicant = applicant
        ticket.maintainer = maintainer
        ticket.status = '审批中'
        ticket.save()
        return instance


class ConsumerRegisterApplySerializer(ApplySerializer):
    
    class Meta:
        model = ConsumerRegisterApply
        fields = '__all__'


class ConsumerOrderApplySerializer(ApplySerializer):
    
    class Meta:
        model = ConsumerOrderApply
        fields = '__all__'


class ConsumerTrialApplySerializer(ApplySerializer):
    
    def create(self, validated_data):
        # todo 定义审批流程
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

