from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tickets.views import ConsumerTrialApplyViewSet, ConsumerLaunchApplyViewSet, VendorApplyViewSet, \
    VendorApiApplyViewSet, ProductLaunchApplyViewSet

router = DefaultRouter()

router.register('consumer_trial_apply', ConsumerTrialApplyViewSet, basename='consumer_trial_apply')
router.register('consumer_launch_apply', ConsumerLaunchApplyViewSet, basename='consumer_launch_apply')
router.register('vendor_apply', VendorApplyViewSet, basename='vendor_apply')
router.register('vendor_api_apply', VendorApiApplyViewSet, basename='vendor_api_apply')
router.register('product_launch_apply', ProductLaunchApplyViewSet, basename='product_launch_apply')

urlpatterns = [
    path('', include(router.urls)),
]
