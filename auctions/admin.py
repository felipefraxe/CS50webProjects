from django.contrib import admin
from .models import User, Category, Item, Bid, Comment

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    filter_horizontal = ("watchers",)

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
admin.site.register(Bid)
admin.site.register(Comment)