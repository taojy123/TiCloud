from django.http import HttpResponseRedirect
from django.shortcuts import render

from rest_framework import viewsets
from django_filters import rest_framework as filters

from tickets.models import ConsumerTrialApply, ConsumerLaunchApply, VendorApply, VendorApiApply
from tickets.serializers import ConsumerTrialApplySerializer, ConsumerLaunchApplySerializer, VendorApplySerializer, \
    VendorApiApplySerializer


def redirect_to_doc(request):
    return HttpResponseRedirect('/static/docs/api.html')


class ConsumerTrialApplyFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(fields=['id', 'username'])

    class Meta:
        model = ConsumerTrialApply
        fields = {
            'id': ['exact', 'in'],
            'creator': ['exact'],
            'creator_department': ['exact'],
            'org_name_zh': ['icontains'],
            'org_name_en': ['icontains'],
            'org_number': ['exact']
        }


class ConsumerTrialApplyViewSet(viewsets.ModelViewSet):
    serializer_class = ConsumerTrialApplySerializer
    filter_class = ConsumerTrialApplyFilter
    queryset = ConsumerTrialApply.objects.order_by('id')


class ConsumerLaunchApplyFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(fields=['id', 'username'])

    class Meta:
        model = ConsumerLaunchApply
        fields = {
            'id': ['exact', 'in'],
            'creator': ['exact'],
            'creator_department': ['exact'],
            'org_name_zh': ['icontains'],
            'org_name_en': ['icontains'],
            'org_number': ['exact']
        }


class ConsumerLaunchApplyViewSet(viewsets.ModelViewSet):
    serializer_class = ConsumerLaunchApplySerializer
    filter_class = ConsumerLaunchApplyFilter
    queryset = ConsumerLaunchApply.objects.order_by('id')


class VendorApplyFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(fields=['id', 'org_code'])

    class Meta:
        model = VendorApply
        fields = {
            'id': ['exact', 'in'],
            'creator': ['exact'],
            'creator_department': ['exact'],
            'org_name_zh': ['icontains'],
            'org_code': ['icontains'],
        }


class VendorApplyViewSet(viewsets.ModelViewSet):
    serializer_class = VendorApplySerializer
    filter_class = VendorApplyFilter
    queryset = VendorApply.objects.order_by('id')


class VendorApiApplyFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(fields=['id', 'org_code'])

    class Meta:
        model = VendorApiApply
        fields = {
            'id': ['exact', 'in'],
            'creator': ['exact'],
            'creator_department': ['exact'],
            'org_code': ['icontains'],
            'product_name': ['icontains'],
            'api_code': ['icontains'],
        }


class VendorApiApplyViewSet(viewsets.ModelViewSet):
    serializer_class = VendorApiApplySerializer
    filter_class = VendorApiApplyFilter
    queryset = VendorApiApply.objects.order_by('id')



