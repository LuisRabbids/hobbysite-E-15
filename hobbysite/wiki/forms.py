# wiki/forms.py
from django import forms
from .models import Article, Comment, ArticleCategory

class ArticleForm(forms.ModelForm):
    
    category = forms.ModelChoiceField(queryset=ArticleCategory.objects.all(), empty_label="Select a Category")

    class Meta:
        model = Article
        fields = ['title', 'category', 'entry', 'header_image'] 
        widgets = {
            'entry': forms.Textarea(attrs={'rows': 10, 'cols': 40}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry']
        widgets = {
            'entry': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add your comment...'}),
        }
        labels = {
            'entry': '' 
        }