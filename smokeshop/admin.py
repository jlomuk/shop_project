from django.contrib import admin

from smokeshop.models import Product, Category, Feedback


admin.site.site_title = "Магазин"
admin.site.site_header = "Магазин"
admin.site.index_title = "Магазин табака"


class ProductFeedbackInline(admin.StackedInline):
    model = Feedback
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',), }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'maker_country', 'is_nicotine',
                    'strength', 'smoking', 'taste', 'price', 'available')
    list_filter = ('name', 'brand', 'price', 'strength', 'smoking')
    prepopulated_fields = {'slug': ('name',), }
    list_editable = ('price', 'available')
    search_fields = ('name', '=maker_country', '=brand')
    inlines = (ProductFeedbackInline, )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'rating', 'created')
    list_filter = ('author', 'rating', 'created')
    search_fields = ('=author',)
