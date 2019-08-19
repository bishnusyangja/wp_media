from rest_framework.routers import DefaultRouter

from panel.views import UserAPIView, PlanAPIView, CustomerAPIView, WebSiteAPIView

router = DefaultRouter()
router.register(r'user', UserAPIView, base_name = 'api_leads')
router.register(r'plan', PlanAPIView, base_name = 'api_crm_attachments')
router.register(r'customer', CustomerAPIView, base_name = 'api_contacts')
router.register(r'website', WebSiteAPIView, base_name = 'api_lead_interests')

urlpatterns = router.urls

