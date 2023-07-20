from rest_framework import serializers
from .models import Contact, Product, NetworkNode

# Сериализатор для модели Contact
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


# Сериализатор для модели Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# Сериализатор для модели NetworkNode
class NetworkNodeSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer()  # Вложенный сериализатор для связи с моделью Contact
    products = ProductSerializer(many=True)  # Вложенный сериализатор для связи с моделью Product (разрешает несколько продуктов)

    class Meta:
        model = NetworkNode
        fields = '__all__'

    def create(self, validated_data):
        # Получаем данные для поля contacts и products
        contacts_data = validated_data.pop('contacts')
        products_data = validated_data.pop('products')

        # Создаем экземпляр контакта (Contact)
        contacts_serializer = ContactSerializer(data=contacts_data)
        if contacts_serializer.is_valid():
            contacts = contacts_serializer.save()
        else:
            raise serializers.ValidationError(contacts_serializer.errors)

        # Создаем список продуктов (Product)
        products = []
        for product_data in products_data:
            product_serializer = ProductSerializer(data=product_data)
            if product_serializer.is_valid():
                product = product_serializer.save()
                products.append(product)
            else:
                raise serializers.ValidationError(product_serializer.errors)

        # Создаем экземпляр сетевого звена (NetworkNode)
        network_node = NetworkNode.objects.create(contacts=contacts, **validated_data)

        # Добавляем продукты к созданному сетевому звену
        network_node.products.set(products)

        return network_node
