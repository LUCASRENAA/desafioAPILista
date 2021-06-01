import datetime
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import models
from datetime import  datetime, timezone, timedelta
import requests
import json



import time

# Create your views here.



# Create your views here
from django.views.decorators.csrf import csrf_exempt

from core.models import Lista, Itens, Tokens, Respostas


def login_user(request):
    return render(request,'login.html')


def registro(request):
    return render(request,'registro.html')



def logout_user(request):
    logout(request)
    return redirect('/')
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username != "":
            usuario = authenticate(username=username,password=password)
            if usuario is not None:
                login(request,usuario)
                messages.error(request,"Usuário ou senha invalido")
            else:
                messages.error(request, "Usuário ou senha invalido")
        else:
            email = request.POST.get('email')
            print("aqui")
            print(email)

            username = str(User.objects.get(email=email))
            if username != "":
                usuario = authenticate(username=username, password=password)
                if usuario is not None:
                    login(request, usuario)
                    return redirect('/')
                else:
                    messages.error(request, "Usuário ou senha invalido")



    return  redirect('/')

def submit_registro(request):
    print(request.POST)
    if request.POST:
        senha = request.POST.get('password')
        usuario = request.POST.get ( 'username' )
        email =   request.POST.get ( 'email' )
        try:
            print("e aqui?")
            user = User.objects.create_user ( str(usuario), str(email) ,  str(senha) )




        except:
            User.objects.get(usuario = usuario)
            User.objects.get(email = email)


            return HttpResponse('{"erro":"Usuario já cadastrado"}')

        print("hey")
        return redirect('/')
    return HttpResponse('{"erro":"faça um post"}')


@login_required(login_url='/login/')
def inicio(request):
    listas = Lista.objects.all()
    itens = Itens.objects.all()
    usuario = request.user
    usuario = User.objects.get(username=usuario)
    if usuario.is_staff:
        return render(request,'inicio.html',{'listas':listas,'itens':itens})
    else:
        return redirect('/')

@login_required(login_url='/login/')
def inicio_submit(request,id,tipo):
    usuario = request.user
    usuario = User.objects.get(username=usuario)
    if usuario.is_staff:
        if request.POST:
            titulo = request.POST.get('titulo')
            data_evento = request.POST.get('data_evento')
            tipo2 = request.POST.get('tipo')
            id2 = request.POST.get('id2')

            print("aqui tipo2" + str(tipo2))
            if tipo2 != str(1):
                tipo = tipo2
            username_lista = request.user
            username_lista = User.objects.get(username = username_lista)

            if tipo == str(1):
                try:
                    Lista.objects.get(titutlo=titulo)
                    return HttpResponse('{"erro":"Lista com esse titulo já existe"}')
                except:
                    Lista.objects.create(titulo=titulo,data_evento=data_evento,usuario=username_lista)

            if tipo == str(2):
                lista = Lista.objects.get(id=int(id2))
                if data_evento != "":
                    lista.data_evento = data_evento
                if titulo != "":
                    lista.titulo = titulo
                lista.save()
        if tipo == str(3):
                Lista.objects.get(id=id).delete()




    return redirect('/inicio')

@login_required(login_url='/login/')
def lista_submit(request):

    if request.POST:
        print("alo")
        return redirect('/')
        #username = request.POST.get('username')



    return render(request,'inicio.html')


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        dlist = []
        d = {}
        lista = Lista.objects.all()
        for listas in lista:
            d["titulo"] = str(listas.titulo)
            d["data"] = str(listas.data_evento)
        dlist.append(d)

        jsonresultado = json.dumps(dlist)
    return HttpResponse(jsonresultado)

'''
    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''

@csrf_exempt
def lista_id(request,id):
    if request.method == "GET":
        if int(id) == 0:

            dlist = []

            for lista in Lista.objects.all():
                d = {}

                d["titulo"]= str(lista.titulo)
                d["data"] =  str(lista.get_data_evento())
                d["id"] =  str(lista.id)

                dlist.append(d)

            sorted_list = sorted(dlist, key=lambda k: (k['data']), reverse=True)
            jsonresultado = json.dumps(sorted_list)
            return HttpResponse(jsonresultado)





        else:
            lista = Lista.objects.get(id=id)
            lista_json = {
                "titulo":str(lista.titulo),
                "data": str(lista.get_data_evento())
            }
            print(lista_json)
            lista_json = json.dumps(lista_json)
            return HttpResponse(lista_json)
    if request.method == "POST":

        response = json.loads(request.body)
        ano = int(response["ano"])
        mes = int(response["mes"])
        dia = int(response["dia"])

        data = datetime(ano, mes, dia, 0, 0)
        token = response["token"]
        print(token)
        print(Tokens.objects.get(token=token))
        UserLista = Tokens.objects.get(token=token).usuario
        UserLista = User.objects.get(username=UserLista)
        titulo = response["titulo"]
        try:
            Lista.objects.get(titutlo=titulo)
            return HttpResponse('{"erro":"Lista com esse titulo já existe"}')
        except:
            Lista.objects.create(titulo=titulo, data_evento=data, usuario=UserLista)


        return HttpResponse(response)
    if request.method == "PUT":
        print("put")
        lista = Lista.objects.get(id=id)
        response = json.loads(request.body)
        titulo = response["titulo"]
        ano = int(response["ano"])
        mes = int(response["mes"])
        dia = int(response["dia"])

        data = datetime(ano, mes, dia, 0, 0)
        print(data)
        if titulo != "":
            lista.titulo = titulo
        if data != "":
            lista.data_evento = data
        lista.save()

        return HttpResponse(response)
    if request.method == "DELETE":
        lista = Lista.objects.get(id=id)
        lista.delete()
        return HttpResponse('{"sucesso":"ID DELETADO"}')


@csrf_exempt
def item_id(request,id):
    if request.method == "GET":
        if int(id) == 0:

            dlist = []

            for lista in Itens.objects.all():
                d = {}

                d["titulo"]= str(lista.titulo.titulo)
                d["nome"] =  str(lista.nome)
                d["id"] =  str(lista.id)
                print(lista)

                dlist.append(d)

            sorted_list = sorted(dlist, key=lambda k: (k['id']), reverse=True)
            jsonresultado = json.dumps(sorted_list)
            return HttpResponse(jsonresultado)

        else:
            itens = Itens.objects.get(id=id)
            itens_json = {
                "idLista":str(itens.titulo.id),
                "item": str(itens.nome)

            }
            print(itens_json)
            itens_json = json.dumps(itens_json)
            return HttpResponse(itens_json)
    if request.method == "POST":

        response = json.loads(request.body)
        id = response["idLista"]
        item = response["item"]
        try:
            Lista.objects.get(id=int(id))
        except:
            return HttpResponse('{"erro":"Lista não existe"}')
        token = response["token"]
        UserLista = Tokens.objects.get(token = token).usuario
        UserLista = User.objects.get(username=UserLista)

        Itens.objects.create(titulo= Lista.objects.get(id=int(id)),nome=item,usuario=UserLista)

        return HttpResponse(response)
    if request.method == "PUT":
        itens = Itens.objects.get(id=id)
        response = json.loads(request.body)
        id = response["idLista"]
        item = response["item"]

        try:
            Lista.objects.get(id=int(id))
        except:
            return HttpResponse('{"erro":"Lista não existe"}')

        if id != "":
            itens.titulo = Lista.objects.get(id=id)
        if item != "":
            itens.nome = item


        itens.save()

        return HttpResponse(response)
    if request.method == "DELETE":
        lista = Itens.objects.get(id=id)
        try:
            Itens.objects.get(id=int(id))
        except:
            return HttpResponse('{"erro":"Item não existe"}')
        lista.delete()
        return HttpResponse('{"sucesso":"ID DELETADO"}')


@login_required(login_url='/login/')
def responder(request):
    listas = Lista.objects.all()
    itens = Itens.objects.all()
    respostas = Respostas.objects.all()
    usuario = request.user
    usuario = User.objects.get(username=usuario)
    print(usuario.is_staff)
    if usuario.is_staff:
        return render(request,'responder.html',{'listas':listas,'itens':itens,'respostas':respostas})
    else:
        return render(request,'responder.html')


@login_required(login_url='/login/')
def inicio_submit_itens(request,id,tipo):
    usuario = request.user
    usuario = User.objects.get(username=usuario)
    if usuario.is_staff:
        if request.POST:
            lista = request.POST.get('lista')
            item = request.POST.get('item')
            resposta = request.POST.get('resposta')


            item = Itens.objects.create(titulo=Lista.objects.get(titulo=lista),nome=item,usuario=User.objects.get(username = str(request.user)))
            if resposta != "":
                Respostas.objects.create(titulo = item,resposta=resposta,usuario=User.objects.get(username=request.user))




    return redirect('/inicio')

@csrf_exempt
def salvarToken(request):
    import requests
    if request.method == "POST":
        response = json.loads(request.body)
        print(response)
        nome = response["usuario"]
        senha = response["senha"]
        response = requests.post("http://127.0.0.1:8000/^login/", None,
                                 {"username": str(nome), "password": str(senha)}).json()
        usuario = authenticate(username=nome, password=senha)
        if usuario is not None:
            usuario = User.objects.get(username=nome)
            try:
                Tokens.objects.get(usuario=usuario)
            except:
                Tokens.objects.create(token=response["token"], usuario=usuario)
            itens_json = {
                "usuario":str(nome),
                "token":str(response["token"])
            }
            itens_json = json.dumps(itens_json)
            return HttpResponse(itens_json)


        else:
            return HttpResponse("Erro")



@csrf_exempt
def resposta_id(request,id):
    print(request.body)
    if request.method == "GET":
        if int(id) == 0:

            dlist = []


            try:
                response = json.loads(request.body)
                token = response["token"]
            except:
                queryDict = dict(request.GET)

                for a in queryDict:

                    teste = json.loads(a)

                token = teste["token"]
            UserLista = Tokens.objects.get(token=token).usuario
            UserLista = User.objects.get(username=UserLista)

            if UserLista.is_staff:
                for lista in Respostas.objects.all():
                    d = {}

                    d["titulo"]= str(lista.titulo)
                    d["resposta"] =  str(lista.resposta)
                    d["usuario"] =  str(lista.usuario)
                    d["lista"] =  str(lista.titulo.titulo.titulo)


                    d["id"] =  str(lista.id)

                    dlist.append(d)

                sorted_list = sorted(dlist, key=lambda k: (k['id']), reverse=True)
                jsonresultado = json.dumps(sorted_list)
                return HttpResponse(jsonresultado)
            else:
                for lista in Respostas.objects.filter(usuario=UserLista):
                    d = {}

                    d["titulo"]= str(lista.titulo)
                    d["resposta"] =  str(lista.resposta)
                    d["usuario"] =  str(lista.usuario)
                    d["lista"] =  str(lista.titulo.titulo.titulo)

                    d["id"] =  str(lista.id)

                    dlist.append(d)

                sorted_list = sorted(dlist, key=lambda k: (k['id']), reverse=True)
                jsonresultado = json.dumps(sorted_list)
                return HttpResponse(jsonresultado)






        else:
            try:
                response = json.loads(request.body)
                token = response["token"]
                UserLista = Tokens.objects.get(token=token).usuario
                UserLista = User.objects.get(username=UserLista)

                if UserLista.is_staff:
                    respostas = Respostas.objects.get(id=id)
                    itens_json = {
                        "idItem":str(respostas.titulo.id),
                        "resposta": str(respostas.resposta),
                        "usuario": str(respostas.usuario),
                        "lista": str(respostas.titulo.titulo.titulo)

                    }
                    print(itens_json)
                    itens_json = json.dumps(itens_json)
                    return HttpResponse(itens_json)
                else:
                    respostas = Respostas.objects.get(id=id,usuario=UserLista)
                    itens_json = {
                        "idItem": str(respostas.titulo.id),
                        "resposta": str(respostas.resposta),
                        "usuario": str(respostas.usuario),
                        "lista": str(respostas.titulo.titulo.titulo)

                    }
                    print(itens_json)
                    itens_json = json.dumps(itens_json)
                    return HttpResponse(itens_json)

            except:
                return HttpResponse("Erro")

    if request.method == "POST":

        print(request.body)
        response = json.loads(request.body)
        token = response["token"]
        UserLista = Tokens.objects.get(token=token).usuario
        UserLista = User.objects.get(username=UserLista)

        idItem = response["idItem"]
        item = response["resposta"]
        print("aqui")
        try:
            Itens.objects.get(id=int(idItem))
        except:
            print("aqui")
            return HttpResponse('{"erro":"Item não existe"}')


        Respostas.objects.create(titulo= Itens.objects.get(id=int(idItem)),resposta=item,usuario=UserLista)
        print("aqui2")
        return HttpResponse(response)
    if request.method == "PUT":
        respostas = Respostas.objects.get(id=id)
        response = json.loads(request.body)

        idItem = response["idItem"]
        resposta = response["resposta"]

        try:
            Itens.objects.get(id=int(idItem))
        except:
            return HttpResponse('{"erro":"Item não existe"}')

        if id != "":
            respostas.idItem = Itens.objects.get(id=int(idItem))
        if resposta != "":
            respostas.resposta = resposta


        respostas.save()

        return HttpResponse(response)
    if request.method == "DELETE":
        lista = Respostas.objects.get(id=id)
        try:
            Respostas.objects.get(id=int(id))
        except:
            return HttpResponse('{"erro":"Resposta não existe"}')
        lista.delete()
        return HttpResponse('{"sucesso":"ID DELETADO"}')


def verItens(request):
    titulo = request.POST.get('titulo')
    print(titulo)

    return redirect('/verItens/'+str(titulo))

def verItensTitulo(request,titulo):
    titulo_id = Lista.objects.get(titulo=titulo).id
    listas = Itens.objects.filter(titulo=titulo_id)
    dlist = []

    for lista in listas:
        d = {}

        d["titulo"] = str(lista.nome)
        d["id"] = str(lista.id)

        dlist.append(d)

    sorted_list = sorted(dlist, key=lambda k: (k['id']), reverse=True)
    jsonresultado = json.dumps(sorted_list)
    funcao = "function initPage(){"
    carregarPaginaExecutar = " window.onload = initPage;"
    scriptparagrafo = "var paragrafo = document.createElement('p');"
    scriptConteudo = 'console.log(json);paragrafo.innerText = "json[i].nome"'
    criar = 'document.getElementById("paragrafo").appendChild(paragrafo);}'

    script =  "for(var i = 0; i < parseInt(json.length); i++){"
    fim = "}</script>"
    return HttpResponse("<script>json = " + str(jsonresultado) + "</script><script>"+ str(funcao) + str(script)+str(scriptparagrafo) + str(scriptparagrafo + str(criar)) + str(fim))


def acao(request):
    print(request.POST)
    import requests
    payload ={"idItem":"4","resposta":"alooo","token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjIyMDY4NjM5LCJlbWFpbCI6IiJ9.NToyMSaSnXGDW3GUpNqFFwmKwQ8leGYMOLpMv1Z0l7c"}

    resposta = requests.post("http://127.0.0.1:8000/resposta/1", data=payload)
    print(resposta)


    return redirect('/')