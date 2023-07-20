from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationView, UserLogoutView, UserViewSet, LoginViews

# Создаем объект router для представления UserViewSet
router = DefaultRouter()
router.register(r'profile', UserViewSet)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='api-register'),
    path('login/', LoginViews.as_view(), name='api-login'),
    path('logout/', UserLogoutView.as_view(), name='api-logout'),

    # Подключаем URL-пути для представления UserViewSet
    path('', include(router.urls)),
]
