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

    def update(self, instance, validated_data):
        # Обновляем поля на верхнем уровне модели NetworkNode
        instance.name = validated_data.get('name', instance.name)
        instance.debt = validated_data.get('debt', instance.debt)
        instance.save()

        # Обновляем вложенные объекты, если они были предоставлены в запросе
        contacts_data = validated_data.get('contacts')
        if contacts_data:
            contacts_serializer = ContactSerializer(instance.contacts, data=contacts_data)
            contacts_serializer.is_valid(raise_exception=True)
            contacts_serializer.save()

        products_data = validated_data.get('products')
        if products_data:
            # Мы не можем просто обновить продукты напрямую, так как это поле связано с many-to-many отношением.
            # Поэтому сначала удаляем все существующие связи с продуктами, а затем добавляем новые продукты.
            instance.products.clear()
            for product_data in products_data:
                product_serializer = ProductSerializer(data=product_data)
                product_serializer.is_valid(raise_exception=True)
                product = product_serializer.save()
                instance.products.add(product)

        return instance
