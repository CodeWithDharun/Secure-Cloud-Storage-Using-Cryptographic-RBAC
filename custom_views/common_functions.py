from django.shortcuts import render, HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from ERP.models import *
from ERP.serializers.serializers import *
from rest_framework.decorators import api_view
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from datetime import datetime
import json


def session_user_id(request):
	user = request.user
	return User.objects.get(pk=user.id);

def session_userid(request):
	user = request.user
	
	user = User.objects.get(pk=user.id)
	return user.id;

def session_useremail(request):
	user = request.user
	return user.email;



def convert_date(date):
    #return "Something"
    return datetime.date.strftime("%d-%m-%Y")


