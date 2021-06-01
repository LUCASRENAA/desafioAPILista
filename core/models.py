from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Lista(models.Model):
    titulo = models.CharField(max_length=100)
    data_evento = models.DateTimeField()
    usuario =  models.ForeignKey(User,models.CASCADE)
    data_criacao = models.DateTimeField(auto_now=True)

    def get_data_evento(self):
        return self.data_evento.strftime('%d/%m/%Y')
class Itens(models.Model):
    titulo = models.ForeignKey(Lista,models.CASCADE)
    usuario =  models.ForeignKey(User,models.CASCADE)
    nome = models.CharField(max_length=100)
    data_evento = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Tokens(models.Model):
    usuario =  models.ForeignKey(User,models.CASCADE)
    token = models.CharField(max_length=100)
    data_evento = models.DateTimeField(auto_now=True)


class Respostas(models.Model):
    usuario =  models.ForeignKey(User,models.CASCADE)

    titulo =  models.ForeignKey(Itens,models.CASCADE)
    resposta = models.CharField(max_length=100)
    data_evento = models.DateTimeField(auto_now=True)


# Create your models here.
