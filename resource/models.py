from django.db import models
from user.models import *


# Create your models here.

class Resource(models.Model):
    resourceName = models.CharField(max_length=100)
    resourceType = models.CharField(max_length=100)
    resource = models.FileField(upload_to="upload/")
    keywords = models.CharField(max_length=200)
    score = models.IntegerField()
    resourceDesc = models.TextField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="resources", blank=True)
    upload_time = models.DateTimeField(auto_now=True)
    ext = models.CharField(max_length=100, blank=True, null=True)
    resourceSize = models.IntegerField(blank=True, null=True)
    content_type = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = "t_resource"


class ResourceComment(models.Model):
    content = models.TextField()
    star = models.IntegerField()
    comment_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments", blank=True)
    res = models.ForeignKey(to=Resource, on_delete=models.CASCADE, related_name="comments", blank=True)

    class Meta:
        db_table = "t_resource_comment"
