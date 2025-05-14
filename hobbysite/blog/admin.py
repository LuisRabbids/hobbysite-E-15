from django.contrib import admin
from blog.models import ArticleCategory, Article, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_on', 'updated_on')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'entry', 'created_on', 'updated_on')
    list_filter = ('author', 'created_on')


admin.site.register(ArticleCategory)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
