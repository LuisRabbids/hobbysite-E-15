from django.contrib import admin
from blog.models import ArticleCategory, Article, Comment


# Not necessary according to specs, but helps in organizing entries
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_on', 'last_updated')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'entry', 'created_on', 'last_updated')
    list_filter = ('author', 'created_on')


admin.site.register(ArticleCategory)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment,CommentAdmin)
