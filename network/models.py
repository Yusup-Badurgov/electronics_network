from django.db import models


class Contact(models.Model):
    """
    Модель для хранения контактной информации.

    Attributes:
        email (EmailField): Email контакта.
        country (CharField): Страна контакта.
        city (CharField): Город контакта.
        street (CharField): Улица контакта.
        house_number (IntegerField): Номер дома контакта.

    Meta:
        verbose_name (str): Человекочитаемое название модели (единственное число).
        verbose_name_plural (str): Человекочитаемое название модели (множественное число).
    """

    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.IntegerField()

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return self.email


class Product(models.Model):
    """
    Модель для хранения информации о продукте.

    Attributes:
        name (CharField): Название продукта.
        model (CharField): Модель продукта.
        release_date (DateField): Дата выпуска продукта.
    """

    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    release_date = models.DateField()

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name


class NetworkNode(models.Model):
    """
    Модель для хранения информации о сетевом звене.

    Attributes:
        name (CharField): Название сетевого звена.
        contacts (OneToOneField): Контактная информация для сетевого звена.
        products (ManyToManyField): Продукты, связанные с сетевым звеном.
        supplier (ForeignKey): Поставщик, связанный с сетевым звеном (может быть пустым).
        debt (DecimalField): Задолженность сетевого звена.
        created_at (DateTimeField): Дата создания записи о сетевом звене.
    """

    name = models.CharField(max_length=100)
    contacts = models.OneToOneField(Contact, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    supplier = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    debt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Сетевое звено"
        verbose_name_plural = "Сетевые звенья"

    def __str__(self):
        return self.name
