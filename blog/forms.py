from django import forms

from blog.models import Article, Comment, Reply


class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('authors', 'author')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('message',)


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('message',)
