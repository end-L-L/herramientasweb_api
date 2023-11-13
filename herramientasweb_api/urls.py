"""point_experts_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from herramientasweb_api.views import bootstrap
from herramientasweb_api.views import users
from herramientasweb_api.views import materias
from herramientasweb_api.views import auth

urlpatterns = [
    #Admin
        path('admin/', admin.site.urls),
    #Version
        path('bootstrap/version', bootstrap.VersionView.as_view()),
    #Create User
        path('users/', users.UsersView.as_view()),
    #User Data
        path('lista-users/', users.UsersAll.as_view()),
    #Edit User
        path('users-edit/', users.UsersViewEdit.as_view()),
    #Login
        path('token/', auth.CustomAuthToken.as_view()),
    #Logout
        path('logout/', auth.Logout.as_view()),

    #Create Subjects
        path('materia/', materias.MateriaView.as_view()),
    #Show Subjects
        path('lista-materias/', materias.MateriasAll.as_view()),
    #Edit Subjects
        path('materia-edit/', materias.MateriaViewEdit.as_view()),
    
]
