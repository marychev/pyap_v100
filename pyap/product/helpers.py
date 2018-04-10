from .models import Product


class ProductHelper(Product):
    """Хелпер к Главному товару"""
    
    class Meta:
        abstract = True

    @staticmethod
    def get_new(count=12):
        return Product.objects.filter(is_show=True, is_new=True).order_by('?')[:count]

    @staticmethod
    def get_bestseller(count=12):
        return Product.objects.filter(is_show=True, is_bestseller=True).order_by('?')[:count]
