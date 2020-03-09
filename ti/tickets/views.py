import random

from django.http import HttpResponseRedirect
from django.shortcuts import render

from rest_framework import viewsets, exceptions
from django_filters import rest_framework as filters
from rest_framework.decorators import list_route, action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from tickets.models import ConsumerTrialApply, VendorApply, VendorApiApply, ProductLaunchApply, \
    Ticket, User, ConsumerRegisterApply, ConsumerOrderApply
from tickets.serializers import ConsumerTrialApplySerializer, VendorApplySerializer, \
    VendorApiApplySerializer, ProductLaunchApplySerializer, TicketSerializer, UserSerializer, \
    ConsumerRegisterApplySerializer, ConsumerOrderApplySerializer


def redirect_to_doc(request):
    return HttpResponseRedirect('/static/docs/api.html')


class UserFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(fields=['id', 'username'])

    class Meta:
        model = User
        fields = {
            'full_name': ['icontains'],
        }


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    filter_class = UserFilter
    queryset = User.objects.order_by('id')
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def myself(self, request):
        """
        获取当前登录用户信息
        通过传入的 token 判断当前用户，并返回用户信息
        RESPONSE
        请求返回数据结构参考用户列表接口
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    

class ConsumerRegisterApplyFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(fields=['id'])

    class Meta:
        model = ConsumerRegisterApply
        fields = {
            'id': ['exact', 'in'],
        }


class ConsumerRegisterApplyViewSet(viewsets.ModelViewSet):
    serializer_class = ConsumerRegisterApplySerializer
    filter_class = ConsumerRegisterApplyFilter
    queryset = ConsumerRegisterApply.objects.order_by('id')
    
    @action(methods=['GET'], detail=False)
    def make_username(self, request):
        """
        生成可用的用户名
        GET
        short_name: 传入名
        RESPONSE
        根据传入的参数，在后面添加 4 位随机数字，组成 `username` 并返回
        后端保证生成的 `username` 不与系统现存的重复
        如请求返回：`{"username": "abc7824"}`
        """
        short_name = request.query_params.get('short_name', '')
        username = short_name
        for i in range(1000):
            n = random.randint(1000, 9999)
            username = short_name + str(n)
            if not ConsumerRegisterApply.enabled_objects().filter(username=username).exists():
                break
        return Response({'username': username})


class ConsumerOrderApplyFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(fields=['id'])

    class Meta:
        model = ConsumerOrderApply
        fields = {
            'id': ['exact', 'in'],
        }


class ConsumerOrderApplyViewSet(viewsets.ModelViewSet):
    serializer_class = ConsumerOrderApplySerializer
    filter_class = ConsumerOrderApplyFilter
    queryset = ConsumerOrderApply.objects.order_by('id')


class ConsumerTrialApplyFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(fields=['id'])

    class Meta:
        model = ConsumerTrialApply
        fields = {
            'id': ['exact', 'in'],
        }


class ConsumerTrialApplyViewSet(viewsets.ModelViewSet):
    serializer_class = ConsumerTrialApplySerializer
    filter_class = ConsumerTrialApplyFilter
    queryset = ConsumerTrialApply.objects.order_by('id')


class VendorApplyFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(fields=['id'])

    class Meta:
        model = VendorApply
        fields = {
            'id': ['exact', 'in'],
        }


class VendorApplyViewSet(viewsets.ModelViewSet):
    serializer_class = VendorApplySerializer
    filter_class = VendorApplyFilter
    queryset = VendorApply.objects.order_by('id')
    
    @action(methods=['GET'], detail=False)
    def make_org_code(self, request):
        """
        生成可用的机构编码
        GET
        short_name: 传入名
        RESPONSE
        根据传入的参数，在后面添加 4 位随机数字，组成 `org_code` 并返回
        后端保证生成的 `org_code` 不与系统现存的重复
        请求返回：`{"org_code": "abc7824"}`
        """
        short_name = request.query_params.get('short_name', '')
        org_code = short_name
        for i in range(1000):
            n = random.randint(1000, 9999)
            org_code = short_name + str(n)
            if not VendorApiApply.enabled_objects().filter(org_code=org_code).exists():
                break
        return Response({'org_code': org_code})


class VendorApiApplyFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(fields=['id'])

    class Meta:
        model = VendorApiApply
        fields = {
            'id': ['exact', 'in'],
        }


class VendorApiApplyViewSet(viewsets.ModelViewSet):
    serializer_class = VendorApiApplySerializer
    filter_class = VendorApiApplyFilter
    queryset = VendorApiApply.objects.order_by('id')


class ProductLaunchApplyFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(fields=['id'])

    class Meta:
        model = ProductLaunchApply
        fields = {
            'id': ['exact', 'in'],
        }


class ProductLaunchApplyViewSet(viewsets.ModelViewSet):
    serializer_class = ProductLaunchApplySerializer
    filter_class = ProductLaunchApplyFilter
    queryset = ProductLaunchApply.objects.order_by('id')


class TicketFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(fields=['id'])

    class Meta:
        model = Ticket
        fields = {
            'number': ['exact'],
            'title': ['icontains'],
            'status': ['exact'],
            # 'applicant__username': ['exact'],
            # 'maintainer__username': ['exact'],
        }


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    filter_class = TicketFilter
    queryset = Ticket.objects.order_by('id')

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def review(self, request, pk=None):
        """
        审批工单
        只有 `当前审批人` 才能对工单进行审批操作
        POST
        result: 审批结果，可选值 `同意` / `驳回`
        content: 审批意见，可为空
        RESPONSE
        请求返回工单信息
        """
        ticket = self.get_object()
        user = request.user
        result = request.data.get('result')
        content = request.data.get('content', '')
        flow = ticket.current_flow
        if not flow:
            raise exceptions.ParseError('此工单不可审批')
        if not ticket.current_reviewer:
            ticket.current_reviewer = flow.reviewer
            ticket.save()
        assert ticket.current_reviewer == flow.reviewer, f'Ticket#{ticket.id}.current_reviewer 异常'
        if ticket.current_reviewer != user:
            raise exceptions.ParseError('只有 `当前审批人` 才能对工单进行审批操作')
        if result not in ['同意', '驳回']:
            raise exceptions.ParseError('result 必须是 `同意` / `驳回`')
        flow.result = result
        flow.content = content
        flow.save()
        ticket.current_reviewer = None
        if result == '同意':
            if ticket.current_flow:
                ticket.current_reviewer = ticket.current_flow.reviewer
            else:
                ticket.status = '审批通过'
        elif result == '驳回':
            ticket.status = '驳回'
        ticket.save()
        serializer = self.get_serializer(ticket)
        return Response(serializer.data)

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def revoke(self, request, pk=None):
        """
        撤回工单
        只有 `申请人` 才能对工单进行撤回操作
        RESPONSE
        请求返回工单信息
        """
        ticket = self.get_object()
        user = request.user
        if ticket.applicant != user:
            raise exceptions.ParseError('只有 `申请人` 才能对工单进行撤回操作')
        ticket.current_reviewer = None
        ticket.status = '撤回'
        ticket.save()
        serializer = self.get_serializer(ticket)
        return Response(serializer.data)

