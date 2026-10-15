from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from catalog.models import ProductVariant
from .bag import Bag

@require_POST
def bag_add(request):
    bag = Bag(request)
    variant_id = request.POST.get('variant_id')
    if variant_id:
        variant = get_object_or_404(ProductVariant, id=variant_id)
        bag.add(variant_id=variant.id, quantity=1)
    
    if request.headers.get('HX-Request'):
        return render(request, 'bag/bag_drawer.html', {'bag': bag})
    return redirect('catalog:home')

@require_POST
def bag_remove(request, variant_id):
    bag = Bag(request)
    bag.remove(variant_id)
    if request.headers.get('HX-Request'):
        return render(request, 'bag/bag_drawer.html', {'bag': bag})
    return redirect('catalog:home')