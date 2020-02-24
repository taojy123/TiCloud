from django.http import HttpResponseRedirect
from django.shortcuts import render

from rest_framework import viewsets
from django_filters import rest_framework as filters

from tickets.models import ConsumerTrialApply
from tickets.serializers import ConsumerTrialApplySerializer


def redirect_to_doc(request):
    return HttpResponseRedirect('/static/docs/api.html')


class ConsumerTrialApplyFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(fields=['id', 'username'])

    class Meta:
        model = ConsumerTrialApply
        fields = {
            'id': ['exact', 'in'],
            'user_department': ['exact'],
            'creator': ['exact'],
            'org_name_zh': ['icontains'],
            'org_name_en': ['icontains'],
            'org_number': ['exact']
        }


class ConsumerTrialApplyViewSet(viewsets.ModelViewSet):
    serializer_class = ConsumerTrialApplySerializer
    filter_class = ConsumerTrialApplyFilter
    queryset = ConsumerTrialApply.objects.order_by('id')


