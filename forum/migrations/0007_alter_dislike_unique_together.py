# Generated by Django 5.1.3 on 2024-11-12 00:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_dislike'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dislike',
            unique_together={('post', 'user')},
        ),
    ]