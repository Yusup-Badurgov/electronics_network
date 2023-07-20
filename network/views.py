from django.http import QueryDict
from rest_framework import viewsets, filters
from .models import Contact, Product, NetworkNode
from .serializers import ContactSerializer, ProductSerializer, NetworkNodeSerializer


class ContactViewSet(viewsets.ModelViewSet):
    """
    Представление для операций CRUD с моделью Contact.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    Представление для операций CRUD с моделью Product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    Представление для операций CRUD с моделью NetworkNode.
    """
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['contacts__country']

    def update(self, request, *args, **kwargs):
        """
        Пользовательский метод обновления сетевого звена.

        При обновлении запроса, исключает поле 'supplier' из данных запроса.

        Parameters:
            request (Request): Входящий запрос.
            *args: Позиционные аргументы.
            **kwargs: Именованные аргументы.

        Returns:
            Response: Ответ на запрос обновления сетевого звена с обновленными данными.
        """
        # Создаем копию словаря с данными запроса
        # Создание копии предотвращает изменение исходных данных, чтобы не вносить изменения в данные запроса напрямую.
        mutable_data = request.data.copy()

        # Проверяем, содержится ли 'supplier' в mutable_data и удаляем его
        # Это выполняется потому, что мы хотим обновить сетевое звено без изменения поля 'supplier', если оно было передано в запросе.
        if 'supplier' in mutable_data:
            del mutable_data['supplier']

        # Создаем новый объект QueryDict с обновленными данными
        # QueryDict - это специальный класс Django, используемый для представления данных запроса с параметрами, переданными в URL или теле запроса.
        # Мы обновляем новый QueryDict данными из mutable_data, которые были отфильтрованы на предыдущем шаге. Теперь updated_query_dict содержит все данные, полученные из запроса за исключением поля 'supplier'.
        updated_query_dict = QueryDict('', mutable=True)
        updated_query_dict.update(mutable_data)

        # Присваиваем обновленные данные атрибуту GET объекта request._request
        request._request.GET = updated_query_dict

        # Продолжаем обработку запроса с обновленными данными
        return super().update(request, *args, **kwargs)
