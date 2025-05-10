from django.contrib import admin
from blog.models import ArticleCategory, Article, Comment

# Not necessary according to specs, but helps in organizing entries
class ArticleAdmin(admin.ModelAdmin):
    list_display =('title','category', 'created_on', 'last_updated')

admin.site.register(ArticleCategory)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)

