from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tickets.views import ConsumerTrialApplyViewSet, VendorApplyViewSet, \
    VendorApiApplyViewSet, ProductLaunchApplyViewSet, TicketViewSet, UserViewSet, ConsumerRegisterApplyViewSet, \
    ConsumerOrderApplyViewSet

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('consumer_register_applies', ConsumerRegisterApplyViewSet, basename='consumer_register_applies')
router.register('consumer_order_applies', ConsumerOrderApplyViewSet, basename='consumer_order_applies')
router.register('consumer_trial_applies', ConsumerTrialApplyViewSet, basename='consumer_trial_applies')
router.register('vendor_applies', VendorApplyViewSet, basename='vendor_applies')
router.register('vendor_api_applies', VendorApiApplyViewSet, basename='vendor_api_applies')
router.register('product_launch_applies', ProductLaunchApplyViewSet, basename='product_launch_applies')
router.register('tickets', TicketViewSet, basename='tickets')

urlpatterns = [
    path('', include(router.urls)),
]
