from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    offer = models.DecimalField(max_digits=5, decimal_places=2)
    packing = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name


class Variant(models.Model):
    product = models.ForeignKey(Product, related_name='variants',on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    packing = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.description}"


class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class SalesOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE,null=True)
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.customer.name}"
