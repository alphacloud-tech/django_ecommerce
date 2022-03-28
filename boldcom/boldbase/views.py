from django.shortcuts import render
from store.models import Product

# Create your views here.


def home(request):
    # ===> we are showing only the products that are available
    # ===> we are showing the products that are available only
    products = Product.objects.all().filter(is_available=True)
    
    context  = {
        'products' : products
    }
    return render(request, 'boldbase/home.html', context )
