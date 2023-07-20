from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, ProductViewSet, NetworkNodeViewSet

router = DefaultRouter()
router.register(r'contacts', ContactViewSet)
router.register(r'products', ProductViewSet)
router.register(r'network-nodes', NetworkNodeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
