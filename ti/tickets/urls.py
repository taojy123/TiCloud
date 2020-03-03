from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tickets.views import ConsumerTrialApplyViewSet, VendorApplyViewSet, \
    VendorApiApplyViewSet, ProductLaunchApplyViewSet, TicketViewSet, UserViewSet, ConsumerRegisterApplyViewSet, \
    ConsumerOrderApplyViewSet

router = DefaultRouter()

router.register('user', UserViewSet, basename='user')
router.register('consumer_register_apply', ConsumerRegisterApplyViewSet, basename='consumer_register_apply')
router.register('consumer_order_apply', ConsumerOrderApplyViewSet, basename='consumer_order_apply')
router.register('consumer_trial_apply', ConsumerTrialApplyViewSet, basename='consumer_trial_apply')
router.register('vendor_apply', VendorApplyViewSet, basename='vendor_apply')
router.register('vendor_api_apply', VendorApiApplyViewSet, basename='vendor_api_apply')
router.register('product_launch_apply', ProductLaunchApplyViewSet, basename='product_launch_apply')
router.register('ticket', TicketViewSet, basename='ticket')

urlpatterns = [
    path('', include(router.urls)),
]
