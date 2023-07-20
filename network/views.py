from django.http import QueryDict
from rest_framework import viewsets, filters
from .models import Contact, Product, NetworkNode
from .serializers import ContactSerializer, ProductSerializer, NetworkNodeSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['contacts__country']

    def update(self, request, *args, **kwargs):
        # Создаем копию словаря с данными запроса
        mutable_data = request.data.copy()

        # Проверяем, содержится ли 'supplier' в mutable_data и удаляем его
        if 'supplier' in mutable_data:
            del mutable_data['supplier']

        # Создаем новый объект QueryDict с обновленными данными
        updated_query_dict = QueryDict('', mutable=True)
        updated_query_dict.update(mutable_data)

        # Присваиваем обновленные данные атрибуту GET объекта request._request
        request._request.GET = updated_query_dict

        # Продолжаем обработку запроса с обновленными данными
        return super().update(request, *args, **kwargs)
