from category.models import Category


def custom_context(request):
    category_links = Category.objects.all()
    return {'cat_li': category_links}
