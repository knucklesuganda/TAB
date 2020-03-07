from django.db import models

# Create your models here.


class Question(models.Model):
    text = models.TextField(null=False, blank=False, unique=True)
    url = models.URLField(null=True)

    forward = models.IntegerField(null=True, blank=False)
    back = models.IntegerField(null=True, blank=False)
