from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tickets.views import ConsumerTrialApplyViewSet, ConsumerLaunchApplyViewSet

router = DefaultRouter()

router.register('consumer_trial_apply', ConsumerTrialApplyViewSet, basename='consumer_trial_apply')
router.register('consumer_launch_apply', ConsumerLaunchApplyViewSet, basename='consumer_launch_apply')

urlpatterns = [
    path('', include(router.urls)),
]
