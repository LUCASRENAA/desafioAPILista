# Generated by Django 3.0.7 on 2021-05-25 23:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('data_evento', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Itens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resposta', models.CharField(max_length=300)),
                ('titulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Lista')),
            ],
        ),
    ]
