from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


class Announce(models.Model):
    title = models.CharField(max_length=100)
    main_image = models.ImageField(upload_to='announce_images', blank=True, null=True)
    description = models.TextField(blank=True)
    tags = TaggableManager()

    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='announces', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('announce:announce_detail', kwargs={'pk': self.pk})
                     
    class Meta:
        ordering = ['-created']


class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='announce_images', blank=True, null=True)
    announce = models.ForeignKey(Announce, related_name='images', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']


class Comment(models.Model):
    announce = models.ForeignKey(Announce, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='announce_comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']


