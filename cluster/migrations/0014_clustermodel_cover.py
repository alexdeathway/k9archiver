# Generated by Django 3.2.15 on 2023-02-27 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0013_alter_notemodel_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='clustermodel',
            name='cover',
            field=models.ImageField(default='default_cluster_cover.jpg', upload_to='cluster_cover'),
        ),
    ]
