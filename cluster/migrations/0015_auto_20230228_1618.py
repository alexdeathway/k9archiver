# Generated by Django 3.2.15 on 2023-02-28 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0014_clustermodel_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='notemodel',
            name='summary',
            field=models.CharField(default='None', max_length=250),
        ),
        migrations.AlterField(
            model_name='notemodel',
            name='body',
            field=models.TextField(default='Empty', max_length=100000),
        ),
    ]
