from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.core.exceptions import ValidationError
# Create your models here.


def validate_id(value):
    if value not in Question.objects.values('id'):
        raise ValidationError


class Question(models.Model):
    text = models.TextField(null=False, blank=False, unique=True)
    answer = models.TextField(null=False, blank=False)
    url = models.URLField(null=True)

    forward = models.IntegerField(null=True, blank=False, validators=[validate_id])
    back = models.IntegerField(null=True, blank=False, validators=[validate_id])


@receiver(pre_delete, sender=Question, dispatch_uid='question_delete_log')
def pre_delete_question(sender, instance, using, **kwargs):
    if instance.forward:
        Question.objects.get(back=instance.forward).delete()
