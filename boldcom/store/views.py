# from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from store.models import Product
from category.models import Category
from carts.models import CartItem
from django.db.models import Q
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
# ===> so that we can display the categories 
# ===> 
@login_required
def store(request, category_slug=None):
    categories  = None
    products    = None

    # ===> if it is not found bring a 404 error
    # ===> if the slug is not none
    if category_slug != None:
        categories      = get_object_or_404(Category, slug=category_slug)
        products        = Product.objects.filter(category=categories, is_available=True)
        # ===> this paginator will work for each categories products
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        # ===> we are getting the pages products
        paged_products = paginator.get_page(page)
        # ===> count all the available products
        product_count   = products.count()
    else:
        # ===> we are showing only the products that are available
        products = Product.objects.all().filter(is_available=True).order_by('id')
        
         # <===> These codes here works for the paginator  <===>
        # ===> we are passing the products and the numbers of products we wants to show
        # ===> we are capturing the url that comes with the page number, which means from the GET request
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        # ===> we are getting the pages products
        paged_products = paginator.get_page(page)
       
        
        # ===> we are counting the result of the products
        product_count = products.count()
    
        
    context = {
        'products' : paged_products,
        # 'products' : products,
        'product_count': product_count
    }
    
    
    
    return render(request, 'store/store.html', context)


@login_required
def product_detail(request, category_slug, product_slug):
    try:
        # ===> we should be able to see the products detail
        single_product = Product.objects.get(category__slug = category_slug, slug = product_slug)
        
        # ===> check if the product exist in the cartitem
        # ===> 'cart__' this means that we are checking the Cart' model, because the 'Cart' is ForeignKey of the Cartitem
        # ===> and accessing the cart_id
        # ===> '_cart_id(request)' this is the private function we created that stores the session key,
        # ===> we have to import it
        # ===> if this <===> in_cart = CartItem.objects.filter(cart__cart_id =_cart_id(request), product = single_product).exists() <===> returns anything or has any object, it is going to return true, true means that we are not going to show the add to cart button., if false then the product is not in the cart
        in_cart = CartItem.objects.filter(cart__cart_id =_cart_id(request), product = single_product).exists()
        
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
    }
    
    return render(request, 'store/product_detail.html', context )



def search(request):
    # ===> we need to recieve what is coming from the url which is the get request
    # ===> we are checking if the get request has the keyword or not
    # ===> we are storing the value of that 'keyword' inside the keyword = variable
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        # ===> we are also checking if the keyword we are getting from the url is blank or not
        if keyword:
            # ===> '__icontains' means this will look for the whole description and if it found anything related to this '__icontains = keyword' keyword, it will bring that product and show it inside the particular place you are searching it.
            # ===> the 'Q' is the queryset
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains = keyword) | Q(product_name__icontains = keyword))       
            product_count = products.count()
        else:
            return render(request, 'store/store.html')
    
    context = {
        'products' : products,
        'product_count' : product_count,
    }
    
    
    return render(request, 'store/store.html', context)

