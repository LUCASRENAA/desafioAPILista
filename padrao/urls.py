"""controle_estoque URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core import views
from django.views.generic import RedirectView


from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registro/', views.registro),


    path('registro/submit', views.submit_registro),
    path('token/pegar', views.salvarToken),

    path('inicio/',views.inicio),
    path('', views.responder),

    path('inicio/submit/<id>/<tipo>', views.inicio_submit),
    path('inicio/itens/submit/<id>/<tipo>', views.inicio_submit_itens),


    path('login/', views.login_user),
    path('login/submit',views.submit_login),
    path(r'^login/', obtain_jwt_token),
    path('lista/<id>', views.lista_id),
    path('item/<id>', views.item_id),
    path('resposta/<id>', views.resposta_id),
                  path('verItens/', views.verItens),
                    path('verItens/<titulo>',views.verItensTitulo),
                  path('acao/acao', views.acao),

                  path('<qualquercoisa>',RedirectView.as_view(url='inicio/'))


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
