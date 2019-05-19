from django.db import models

# Create your models here.

from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

class AbstractModel(models.Model):
    """
    Base class for common fields
    """
    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True) #may be used for soft delete case

    class Meta:
        abstract = True


class Photo(AbstractModel):
    group       = models.ForeignKey('PhotoGroup',on_delete=models.CASCADE,related_name='photos')
    flickr_id    = models.CharField(max_length=200,verbose_name='Flickr Photo ID')
    title       = models.TextField(blank=True)
    description = models.TextField(null=True,blank=True)
    views       = models.IntegerField(default=0)
    url   = models.URLField(verbose_name='Flickr Photo url')
    tags = models.ManyToManyField('Tag')

    class Meta:
        app_label           = 'flickr'
        verbose_name        = "Photo"
        verbose_name_plural = "Photos"

    def __str__(self):
        return ("{} : {}" .format(self.id,self.flickr_id))


@receiver(post_save, sender=Photo)
def photo_postsave(sender, instance, **kwargs):
    if kwargs['created']:
        #incrementing no of photos if new photo created for that group
        if instance.group:
            instance.group.no_of_photos+=1
            instance.group.save()

class PhotoGroup(AbstractModel):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='photo_groups')
    flickr_id = models.CharField(max_length=200,verbose_name='Flickr Group ID')
    name     = models.TextField(blank=True)
    description = models.TextField(null=True,blank=True)
    no_of_photos = models.IntegerField(default=0)
    url = models.URLField(verbose_name='Flickr Group Icon url')

    class Meta:
        app_label           = 'flickr'
        verbose_name        = "Photo Group"
        verbose_name_plural = "Photo Groups"

    def __str__(self):
        return ("{} : {}" .format(self.id,self.flickr_id))


class Tag(AbstractModel):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)

    class Meta:
        app_label           = 'flickr'
        verbose_name        = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return ("{} : {}" .format(self.id,self.name))
