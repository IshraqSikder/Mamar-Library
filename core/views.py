from django.shortcuts import render
from django.template.defaultfilters import slugify
from posts.models import Post
from categories.models import Category
# Create your views here.

def HomeView(request, category_slug = None):
    data = Post.objects.all()
    if category_slug is not None:
        category = Category.objects.get(slug = category_slug)
        data = Post.objects.filter(category = category)
    categories = Category.objects.all()
    return render(request, 'index.html', {'data' : data, 'category' : categories})