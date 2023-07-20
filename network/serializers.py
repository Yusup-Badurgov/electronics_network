from rest_framework import serializers
from .models import Contact, Product, NetworkNode


class ContactSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Contact.
    """
    class Meta:
        model = Contact
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.
    """
    class Meta:
        model = Product
        fields = '__all__'


class NetworkNodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели NetworkNode.

    Включает в себя вложенные сериализаторы для связанных моделей Contact и Product.
    """

    contacts = ContactSerializer()
    products = ProductSerializer(many=True)

    class Meta:
        model = NetworkNode
        fields = '__all__'

    def create(self, validated_data):
        """
        Метод для создания экземпляра NetworkNode.

        Parameters:
            validated_data (dict): Валидированные данные запроса.

        Returns:
            NetworkNode: Созданный экземпляр NetworkNode.
        """
        contacts_data = validated_data.pop('contacts')
        products_data = validated_data.pop('products')

        # Создаем экземпляр контакта (Contact)
        contacts = Contact.objects.create(**contacts_data)

        # Создаем список продуктов (Product)
        products = [Product.objects.create(**product_data) for product_data in products_data]

        # Создаем экземпляр сетевого звена (NetworkNode)
        network_node = NetworkNode.objects.create(contacts=contacts, **validated_data)

        # Добавляем продукты к созданному сетевому звену
        network_node.products.set(products)

        return network_node
