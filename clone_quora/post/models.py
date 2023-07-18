import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=250)
    descriptions = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    photo = models.ImageField(upload_to='images/', blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(get_user_model(), related_name='author',
                               on_delete=models.CASCADE,
                               )
    created_at = models.DateTimeField(default=datetime.datetime.now, null=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + ' - ' + str(self.created_at))
        super().save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Question(models.Model):
    body_question = models.TextField()
    poster = models.ImageField(upload_to='images/', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.body_question

    def get_absolute_url(self):
        return reverse('question_detail', args=[str(self.id)])


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.TextField()
    poster = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.answer

    def get_absolute_url(self):
        return reverse('question_detail', args=[str(self.id)])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    body = models.TextField(max_length=600)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['-created_at']
