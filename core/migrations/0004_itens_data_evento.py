# Generated by Django 3.0.7 on 2021-05-26 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210526_0846'),
    ]

    operations = [
        migrations.AddField(
            model_name='itens',
            name='data_evento',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
