# Generated by Django 3.2.8 on 2021-12-18 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cluster', '0008_notemodel_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clustermodel',
            name='permission',
            field=models.CharField(choices=[('p', 'Public'), ('PO', 'Participant Only')], default='PO', max_length=10),
        ),
        migrations.CreateModel(
            name='NoteEventModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(choices=[('created', 'created'), ('updated', 'updated'), ('approved', 'approved')], max_length=20)),
                ('event_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='NoteEventModel_User', to=settings.AUTH_USER_MODEL)),
                ('event_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='NoteEventModel_NoteModel', to='cluster.notemodel')),
            ],
        ),
    ]