# Generated by Django 3.1.4 on 2020-12-09 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_codregistro'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]