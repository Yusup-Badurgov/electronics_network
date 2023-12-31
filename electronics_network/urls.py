from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('authentication.urls')),
    path('api/', include('network.urls')),
    # Добавляем URL-паттерны для Swagger документации
    path('', include('swagger')),
]
