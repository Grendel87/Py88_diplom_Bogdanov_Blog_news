from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()
class Article(models.Model):
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='articles/', default='defaults/default.jpeg', blank=True)
    content = RichTextField()
    create_at = models.DateField(auto_now=True)

    authors = models.ManyToManyField('user.CustomUser', through='CollaborationAuthor')
    is_published = models.BooleanField(default=False)


class CollaborationAuthor(models.Model):
    article = models.ForeignKey('blog.Article', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    invitation_accepted = models.BooleanField(default=False)
    is_creator = models.BooleanField(default=False)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name="comment", on_delete=models.CASCADE)
    message = models.TextField(max_length=250)
    create_at = models.DateField(auto_now=True)



class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_replies')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_replies')
    message = models.TextField(max_length=250)
    create_at = models.DateField(auto_now=True)