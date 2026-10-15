from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name_uk = models.CharField(max_length=100, default="Піжами")
    name_en = models.CharField(max_length=100, default="Pyjamas")
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories (Категорії)'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name_uk} / {self.name_en}"

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title_uk = models.CharField(max_length=200, default="Шовкова піжама")
    title_en = models.CharField(max_length=200, default="Silk Pyjama")
    slug = models.SlugField(unique=True, blank=True)
    description_uk = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[self.slug])

    def __str__(self):
        return f"{self.title_uk} ({self.price} ₴)"

class ProductVariant(models.Model):
    SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('ONE SIZE', 'One Size'),
    ]
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    sku = models.CharField(max_length=64, unique=True)
    color = models.CharField(max_length=50, default='Пудра / Blush')
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='S')
    inventory = models.PositiveIntegerField(default=15)

    def __str__(self):
        return f"{self.product.title_uk} — {self.color} ({self.size})"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/')
    alt_text = models.CharField(max_length=150, blank=True)