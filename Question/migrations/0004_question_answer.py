# Generated by Django 3.0.4 on 2020-09-12 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Question', '0003_auto_20200912_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answer',
            field=models.TextField(blank=True),
        ),
    ]
