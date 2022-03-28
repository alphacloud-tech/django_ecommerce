from django.contrib import admin
from .models import Product, Variation
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields  = {'slug': ('product_name',)}


# ===> we want to show the variation properly in the admin panel
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    # ===> we want the 'is_active' to the editable in the select variation table, so that we can disable and enable a color or size
    list_editable = ('is_active',)
    # ===> we also want the filter box in the admin panel so that we can be able to see the categories of products and color, sizes
    list_filter = ('product', 'variation_category', 'variation_value')
    
    


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)