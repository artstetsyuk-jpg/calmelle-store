from django.conf import settings
from catalog.models import ProductVariant

class Bag:
    def __init__(self, request):
        self.session = request.session
        bag = self.session.get(settings.BAG_SESSION_ID)
        if not bag:
            bag = self.session[settings.BAG_SESSION_ID] = {}
        self.bag = bag

    def add(self, variant_id, quantity=1):
        variant_id = str(variant_id)
        if variant_id not in self.bag:
            self.bag[variant_id] = {'quantity': 0}
        self.bag[variant_id]['quantity'] += int(quantity)
        self.save()

    def remove(self, variant_id):
        variant_id = str(variant_id)
        if variant_id in self.bag:
            del self.bag[variant_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        variant_ids = self.bag.keys()
        variants = ProductVariant.objects.filter(id__in=variant_ids).select_related('product')
        for variant in variants:
            item = self.bag[str(variant.id)].copy()
            item['variant'] = variant
            item['price'] = variant.product.price
            item['total_price'] = variant.product.price * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.bag.values())

    def get_total_price(self):
        variants = ProductVariant.objects.filter(id__in=self.bag.keys()).select_related('product')
        return sum(
            variant.product.price * self.bag[str(variant.id)]['quantity']
            for variant in variants
        )

def bag_context(request):
    return {'bag': Bag(request)}