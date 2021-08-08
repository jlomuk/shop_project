class CategoryFilterToSlugMixin:

    def get_queryset(self, *args, **kwargs):
        """
        Миксин для фильтрации товара по конкретному slug'у категории товара
        """
        qs = super().get_queryset(*args, **kwargs)
        if self.kwargs.get('category_slug'):
            qs = qs.filter(category__slug=self.kwargs['category_slug'])
        return qs