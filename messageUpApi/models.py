from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class UserType(models.Model):
    name = models.CharField(max_length=100)
    label = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    user_type = models.ForeignKey(
        UserType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class BusinessCategory(models.Model):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.label


class Business(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    address = models.TextField()
    phone = models.BigIntegerField()
    category = models.ForeignKey(
        BusinessCategory,
        on_delete=models.CASCADE,
        related_name="businesses",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="businesses",
    )
    profile = models.FileField(upload_to="business/profile/")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Status(models.Model):
    image = models.FileField(upload_to="status/")
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="statuses",
    )
    created_at = models.DateTimeField(auto_now_add=True)


class ProductCategory(models.Model):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.label


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.FileField(upload_to="products/main/")
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name="products",
    )
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    description = models.TextField()
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="products",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.FileField(upload_to="products/extra/")


class CartItem(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    quantity = models.IntegerField()


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart",
    )
    items = models.ManyToManyField(CartItem, related_name="carts")


class Order(models.Model):
    items = models.ManyToManyField(CartItem, related_name="orders")
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    price = models.IntegerField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
