class CategoryFilterToSlugMixin:

    def get_queryset(self, *args, **kwargs):
        qs = self.queryset
        if self.kwargs.get('category_slug'):
            qs = qs.filter(category__slug=self.kwargs['category_slug'])
        return qs