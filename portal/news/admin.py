from django.contrib import admin
from .models import Post, Category, PostCategory, Subscription, Author, Comment

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Subscription)


# Register your models here.
