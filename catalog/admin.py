from django.contrib import admin
from .models import Category, Product, ProductVariant, ProductImage

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 2

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_uk', 'name_en', 'slug')
    prepopulated_fields = {'slug': ('name_en',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title_uk', 'category', 'price', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured', 'category')
    prepopulated_fields = {'slug': ('title_en',)}
    inlines = [ProductImageInline, ProductVariantInline]