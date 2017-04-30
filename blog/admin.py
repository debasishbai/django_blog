from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "published_date", "author")
    list_filter = ("published_date", "creation_date")

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
