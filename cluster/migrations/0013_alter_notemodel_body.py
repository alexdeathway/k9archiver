# Generated by Django 3.2.15 on 2023-02-24 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0012_clustergallery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notemodel',
            name='body',
            field=models.CharField(default='Empty', max_length=100000),
        ),
    ]
