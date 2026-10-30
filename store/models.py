from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение товара")
    category = models.CharField(max_length=100, verbose_name="Категория", default="Разное")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
