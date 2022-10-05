from django.contrib import admin
from blog.models import Category, Contact,Comment,Profile,Category
from blog.models import Post

# Register your models here.
admin.site.register(Contact)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Category)
