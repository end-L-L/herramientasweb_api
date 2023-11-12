from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from herramientasweb_api.serializers import *
from herramientasweb_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.dateparse import parse_date
import string
import random
import json

# Obtener Materias Registradas
class MateriasAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        materias = Materia.objects.order_by("nrc")
        lista = MateriasSerializer(materias, many=True).data
        
        return Response(lista, 200)

# Transacciones de Materia
class MateriaView(generics.CreateAPIView):
    
    #Obtener Materia por NRC
    def get(self, request, *args, **kwargs):
        materia = get_object_or_404(Materia, nrc = request.GET.get("nrc"))
        materia = MateriasSerializer(materia, many=False).data

        return Response(materia, 200)

    #Registrar Materia
    @transaction.atomic
    def post(self, request, *args, **kwargs):

        materia = MateriaSerializer(data=request.data)
        
        if materia.is_valid():
            
            nrc = request.data["nrc"]
            
            existing_nrc = Materia.objects.filter(nrc=nrc).first()

            if existing_nrc:
                return Response({"message":"nrc "+nrc+", is already taken"},400)

            materia = Materia.objects.create( nrc = request.data["nrc"],
                                              nombre= request.data["nombre"],
                                              seccion= request.data["seccion"],
                                              dias= request.data["dias"],
                                              horaInicio= request.data["horaInicio"],
                                              horaFin= request.data["horaFin"],
                                              salon= request.data["salon"],
                                              programa= request.data["programa"]
            )

            materia.save()
            return Response({"subject_created_nrc": materia.nrc }, 201)

        return Response(materia.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Actualizar Materia
class MateriaViewEdit(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def put(self, request, *args, **kwargs):
        materia = get_object_or_404(Materia, nrc=request.data["nrc"])
        materia.nombre = request.data["nombre"]
        materia.seccion = request.data["seccion"]
        materia.dias = request.data["dias"]
        materia.horaInicio = request.data["horaInicio"]
        materia.horaFin = request.data["horaFin"]
        materia.salon = request.data["salon"]
        materia.programa = request.data["programa"]
        materia.save()
        mat = MateriasSerializer(materia, many=False).data

        return Response(mat,200)