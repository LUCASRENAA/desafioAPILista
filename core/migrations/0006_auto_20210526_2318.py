# Generated by Django 3.0.7 on 2021-05-27 02:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_lista_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itens',
            name='resposta',
        ),
        migrations.CreateModel(
            name='Respostas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resposta', models.CharField(max_length=100)),
                ('titulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Itens')),
            ],
        ),
    ]