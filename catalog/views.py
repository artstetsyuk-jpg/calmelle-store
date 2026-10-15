from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product

def set_language(request, lang_code):
    if lang_code in ['uk', 'en']:
        request.session['django_language'] = lang_code
    return redirect(request.META.HTTP_REFERER or 'catalog:home')

def home(request):
    lang = request.session.get('django_language', 'uk')
    category_slug = request.GET.get('category')
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True).prefetch_related('images', 'variants')
    
    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=active_category)

    return render(request, 'catalog/list.html', {
        'categories': categories,
        'featured_products': products,
        'active_category': active_category,
        'lang': lang,
    })

def product_detail(request, slug):
    lang = request.session.get('django_language', 'uk')
    product = get_object_or_404(Product, slug=slug, is_active=True)
    variants = product.variants.filter(inventory__gt=0)
    return render(request, 'catalog/detail.html', {
        'product': product,
        'variants': variants,
        'lang': lang,
    })