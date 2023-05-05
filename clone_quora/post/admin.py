from django.contrib import admin
from .models import Post, Category, Question, Answer, Comment
from django.contrib.auth.models import Group, User


# admin.site.register(Followers)
# admin.site.register(Following)

# unregister Group
admin.site.unregister(Group)
admin.site.register(Comment)

# register models.py
admin.site.register(Category)
# admin.site.register(Blog)
admin.site.register(Question)
admin.site.register(Answer)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}









