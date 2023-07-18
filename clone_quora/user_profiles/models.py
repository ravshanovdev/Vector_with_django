from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    biography = models.TextField()
    profile_pic = models.ImageField(upload_to='images/profile/', blank=True)
    web_site_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    pinterest_url = models.CharField(max_length=255, null=True, blank=True)
    follows = models.ManyToManyField("self", related_name="following_by", symmetrical=False, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    USERNAME_FIELD = 'user'
    REQUIRED_FIELDS = []
    # is_anonymous = True
    is_authenticated = True

    def get_full_name(self):
        return self.user.get_full_name()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.first_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return reverse('profile_page', kwargs={'slug': self.slug})

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = self.user.username
    #     super().save(*args, **kwargs)


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])


post_save.connect(create_profile, sender=User)
