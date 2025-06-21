from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from rest_framework.decorators import api_view
from django.contrib.auth.models import Permission, User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.conf import  settings
from django.urls import reverse
from ERP.models import *
from ERP.serializers.serializers import *
#import requests
from ERP.custom_views.common_functions import *


@api_view(['GET','POST'])
def index_create(request):
    print("home")
    if request.method=='GET':

        return Response({'data':''},template_name='ERP/includes/index.html')
    return Response({'data':'success'},template_name='ERP/includes/index.html')


@api_view(['GET','POST'])
def admin_home(request):
    
    if request.method=='GET':
        return Response({'data':''},template_name='ERP/includes/admin_home.html')
    return Response({'data':'success'},template_name='ERP/includes/admin_home.html')
      

@api_view(['GET', 'POST'])
def login_user(request,id):
    value = id
    text = ""
    if value == "1":
        text = "Admin"        
    elif value == "2":
        text = "User"

    if request.method == 'GET':
        return Response({'data':text,"user":value},template_name='ERP/includes/login.html')
    else:

        username = request.POST['username']
        password = request.POST['password']
        logout(request)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['newvariable']='test'
                #return Response({"data": "Data Added Successfully"}, 
                #template_name='ERP/signup.html')
                print("user")
                print(user)
                if user.is_superuser == 1:
                    user_type = 1
                else:
                    user_type = 2
                return Response({'data':user_type},template_name='ERP/includes/home.html')
            
        return render(request, 'ERP/includes/login.html')


@api_view(['GET', 'POST'])
def logout_user(request):

    logout(request)
    
    return HttpResponseRedirect('/erp/index/') 