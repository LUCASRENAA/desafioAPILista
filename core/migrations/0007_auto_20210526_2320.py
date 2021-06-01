# Generated by Django 3.0.7 on 2021-05-27 02:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0006_auto_20210526_2318'),
    ]

    operations = [
        migrations.AddField(
            model_name='lista',
            name='data_criacao',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='respostas',
            name='data_evento',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='respostas',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tokens',
            name='data_evento',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
