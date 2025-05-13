# wiki/admin.py
from django.contrib import admin
from .models import ArticleCategory, Article, Comment 

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_on', 'updated_on')
    list_filter = ('category', 'author', 'created_on')
    search_fields = ('title', 'entry')
    readonly_fields = ('created_on', 'updated_on') 

class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'created_on', 'entry_short')
    list_filter = ('author', 'created_on')
    search_fields = ('entry', 'author__username', 'article__title')

    def entry_short(self, obj):
        return obj.entry[:75] + '...' if len(obj.entry) > 75 else obj.entry
    entry_short.short_description = 'Comment Snippet'


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)