# Generated by Django 3.2.8 on 2021-11-30 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0004_auto_20211127_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='notemodel',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
