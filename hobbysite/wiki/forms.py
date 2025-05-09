# wiki/forms.py
from django import forms
from .models import Article, Comment, ArticleCategory

class ArticleForm(forms.ModelForm):
    # Category will be a dropdown because it's a ForeignKey
    category = forms.ModelChoiceField(queryset=ArticleCategory.objects.all(), empty_label="Select a Category")

    class Meta:
        model = Article
        fields = ['title', 'category', 'entry', 'header_image'] # Author, created_on, updated_on are handled by the view/model
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
            'entry': '' # No label for the comment text area
        }