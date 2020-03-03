from django.http import HttpResponseRedirect
from django.shortcuts import render

from rest_framework import viewsets
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
    
    @action(detail=False, permission_classes=[IsAuthenticated])
    def myself(self, request):
        """
        获取当前登录用户信息
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



