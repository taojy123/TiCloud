from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tickets.views import ConsumerTrialApplyViewSet

router = DefaultRouter()

router.register('consumer_trial_apply', ConsumerTrialApplyViewSet, basename='consumer_trial_apply')

urlpatterns = [
    path('', include(router.urls)),
]
