from django.contrib import admin

from smokeshop.models import Product, Category


admin.site.site_title = "Магазин"
admin.site.site_header = "Магазин"
admin.site.index_title = "Магазин табака"

@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',), }

@admin.register(Product)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'maker_country', 'is_nicotine', 
                    'strength', 'smoking', 'taste', 'price', 'awailable')
    list_filter = ('name', 'brand', 'price', 'strength', 'smoking')
    prepopulated_fields = {'slug': ('name',),}
    search_fields = ('name', '=maker_country', '=brand')