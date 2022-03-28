from distutils.command.upload import upload
from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug    =  models.SlugField(max_length = 200, unique= True)
    description     =  models.TextField(max_length = 500, blank=True)
    price     = models.IntegerField()
    images    = models.ImageField(upload_to = 'photos/products')
    stock  = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category      = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   =  models.DateTimeField(auto_now=True)

    def get_url(self):
        # ===> 'product_detail' is the name passed in the url naming for the templates
        # ===> they are all interconnected
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
    
    
    # ===> variation_manager will allow you to modify the queryset  
class VariationManager(models.Manager):
    def colors(self):
        # ===> this will bring the colors
        return super(VariationManager, self).filter(variation_category = 'color', is_active = True)

    def sizes(self):
        # ===> this will bring the sizes
        return super(VariationManager, self).filter(variation_category = 'size', is_active = True)
    
    
variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)
    
    
    
# ========> Variation model to choose size and color of products that you wants  <========

class Variation(models.Model):
    # ===> we are using 'ForeignKey' because we want to add the variations of each particular products that why we need the Product models as the foreignkey
    # ===> 'on_delete=models.CASCADE' means that when a particular product is deleted, all the variation related to it should also be deleted
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # ===> this will make a dropdown list in the admin panel
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    # ===> incase we wann to disable any of the variation value
    # ===> by default the variation should be active
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    
    
    # ===> we are telling this model that we have created a Variation model
    objects = VariationManager()

    def __str__(self):
        return self.variation_value
    

