from django.http import HttpResponseRedirect
from django.shortcuts import render

from rest_framework import viewsets
from django_filters import rest_framework as filters

from tickets.models import ConsumerTrialApply, ConsumerLaunchApply, VendorApply, VendorApiApply, ProductLaunchApply
from tickets.serializers import ConsumerTrialApplySerializer, ConsumerLaunchApplySerializer, VendorApplySerializer, \
    VendorApiApplySerializer, ProductLaunchApplySerializer


def redirect_to_doc(request):
    return HttpResponseRedirect('/static/docs/api.html')


class ConsumerTrialApplyFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(fields=['id', 'username'])

    class Meta:
        model = ConsumerTrialApply
        fields = {
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


class ProductLaunchApplyFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(fields=['id', 'org_code'])

    class Meta:
        model = ProductLaunchApply
        fields = {
            'creator': ['exact'],
            'creator_department': ['exact'],
            'product_number': ['icontains'],
            'product_name': ['icontains'],
        }


class ProductLaunchApplyViewSet(viewsets.ModelViewSet):
    serializer_class = ProductLaunchApplySerializer
    filter_class = ProductLaunchApplyFilter
    queryset = ProductLaunchApply.objects.order_by('id')



