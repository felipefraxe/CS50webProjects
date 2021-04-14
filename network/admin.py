from django.contrib import admin
from .models import User, Follow, Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ("likes",)

admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Post)