from django.db import models
from categories.models import Category
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField(default = None)
    category = models.ManyToManyField(Category) 
    author = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = 'posts/media/uploads/', blank = True, null = True)
    price = models.FloatField()
    borrowers = models.ManyToManyField(User, related_name='borrowed_books', blank=True)
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f'Commented by {self.name}'