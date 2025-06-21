from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.forms import UserCreationForm
from rest_framework.decorators import api_view
from ERP.models import *
from ERP.serializers.serializers import *
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import connection
from ERP.custom_views.common_functions import *
from datetime import datetime
import socket
import ipaddress
from ipaddress import IPv4Address
import os
import cryptography
from cryptography.fernet import Fernet
import re

@api_view(['GET', 'POST'])
def user_login(request):
	if request.method == 'GET':
		return render(request, 'ERP/user/user_login.html')
	else:
		username = request.POST['username']
		password = request.POST['password']
		#logout(request)
		user = authenticate(username=username, password=password)
		print(user)
		if user is not None:
			if user.is_active:
				login(request, user)
				request.session['newvariable']='test'
# 				return Response({"data": "Data Added Successfully"},
#                             template_name='ERP/signup.html')
				return HttpResponseRedirect('/erp/user/home/')
			
		return render(request, 'ERP/user/user_login.html')


@api_view(['GET','PUT','POST'])
def list_user(request):
    custom_filter={}
    custom_filter['is_superuser']=0

    project_obj = User.objects.filter(**custom_filter)
    project_data = UserSerializer(project_obj, many=True).data
    if request.accepted_renderer.format == 'html':
        return Response({"data": project_data,'module':'Group'},template_name='ERP/user/list.html')
    return Response({"data": project_data})


@api_view(['GET','POST'])
def user_home(request):
    print("home")
    if request.method=='GET':

        return Response({'data':''},template_name='ERP/user/user_home.html')
    return Response({'data':'success'},template_name='ERP/user/user_home.html')
    
@api_view(['GET', 'POST'])
def signup_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("Form VAlid")
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            userobj=User.objects.get(username=user)
            #userobj.email=request.POST['email']
            #userobj.first_name=request.POST['first_name']
            
            #userobj.is_active=1
            #userobj.save()
            print(user)
            mobile = request.POST['mobile']
            role=request.POST['role']
            hint_ques=request.POST['hint_ques']
            hint_ans=request.POST['hint_ans']
            
            profile_data={
                    'user':userobj.id,
                    'mobile':mobile,
                    'role':role,
                    'hint_ques':hint_ques,
                    "hint_ans":hint_ans
                    }

            profile_serializer = TblprofileSerializer(data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save() 
                       
            return Response({"success_data": "Data Added Successfully",'module':'User'},template_name='ERP/user/create_update.html')
        else:
            print("Form not valid")
            return Response({"errors": form.errors},template_name='ERP/user/create_update.html')
    else:
        form = UserCreationForm()
                

    return render(request, 'ERP/user/create_update.html', {'form': form, 'module':'User'})

@api_view(['GET','PUT','POST'])
def list_doc_user(request):
    custom_filter={}
    custom_filter['deleted']=0
    login_user=session_user_id(request)

    obj = Tbldocument.objects.filter(**custom_filter)
    data = TbldocumentSerializer(obj, many=True).data

    check_val = 0
    s = ":"
    local_ip_address = ""
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    my_ip_add = socket.gethostbyname(socket.gethostname())
    ## getting the hostname by socket.gethostname() method
    hostname = socket.gethostname()
    ## getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)
    ## printing the hostname and ip_address
    userid = login_user.id
    print(userid)
    print("Hostname:", hostname)
    print("IP Address: ",ip_address)
    list1 = my_ip_add.split(".")
    print("list")
    print(list1)
    local_ip_address = s.join(list1)
    print(local_ip_address)
    print(type(local_ip_address))
    custom_filter={}
    custom_filter['user_id']=userid
    # custom_filter['ip_address']=local_ip_address
    role = 0
    access_value = 0
    #print(custom_filter)

    ob = Tblaccess.objects.get(**custom_filter)
    print("obj")
    print(ob)



    try:

        obj=Tblaccess.objects.get(**custom_filter)
        print("obj")
        print(obj)

        start_time = obj.start_time
        end_time = obj.end_time
        con_start = datetime.strptime(start_time, '%H:%M:%S').time()
        con_end = datetime.strptime(end_time, '%H:%M:%S').time()
        con_now = datetime.strptime(current_time, '%H:%M:%S').time()

        

        if ((con_now > con_start) and (con_now < con_end)):
            print("Valid")
            check_val = 1
        else :
            check_val = 0
            print("Not Valid")


    except:
        check_val = 0
        print("except")

    role_obj=Tblprofile.objects.get(user_id=userid)
    role = role_obj.role
    print("role")
    print(role)
    print("check_val")
    print(check_val)
    
    if (role == "1"):
        access_value = "1"
    elif((role != "1") and (check_val == 1)):
        access_value = "2"
    else:
        access_value = "3"

    print("access_value")
    print(access_value)
    if request.accepted_renderer.format == 'html':
        return Response({"data": data,"role":role,"access_value":access_value,"userid":userid},template_name='ERP/user/doc_list.html')
    return Response({"data": data})


def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    print("encrypt")
    
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
        
    # encrypt data
    encrypted_data = f.encrypt(file_data)
    
    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)


def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data

    decrypted_data = f.decrypt(encrypted_data)
    # write the original file
    #filepath = "C:/Python37/projects/multiowner/downloads/"
    with open(filename, "wb") as file:
        file.write(decrypted_data)

@api_view(['GET','PUT','POST'])
def doc_request(request):
    custom_filter={}
    custom_filter['deleted']=0
    obj = Tbldocument.objects.filter(**custom_filter)
    data = TbldocumentSerializer(obj, many=True).data
    login_user=session_user_id(request)

    #user_data = Tblaccess.objects.get(user_id = login_user.id )

    if request.method=='GET':
        return Response({'data':data,'module':'doc_request',"userid":login_user.id},template_name='ERP/user/doc_request.html')
    return Response({"data": data})

def send_request(request):
    is_ajax = request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"  
    #if is_ajax:

    #if request.is_ajax() and request.GET['docid']:
    if is_ajax:
        print("entered")
        doc=request.GET['docid']
        login_user=session_user_id(request)

        print(doc)
        
        data = {
        "doc" : doc,
        "user" : login_user.id,
        "doc_request":1
        }
        doc_serializer = TbldocrequestSerializer(data=data)
        if doc_serializer.is_valid():
            doc_serializer.save()
        return HttpResponse(1)

@api_view(['GET','PUT','POST'])
def request_list(request):
    custom_filter={}
    custom_filter['deleted']=0
    
    obj = Tbldocrequest.objects.filter(**custom_filter)
    data = TbldocrequestSerializer(obj, many=True).data

    
    if request.accepted_renderer.format == 'html':
        return Response({"data": data},template_name='ERP/user/request_list.html')
    return Response({"data": data})

def allow_access(request):
    is_ajax = request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
    #if is_ajax:

    #if request.is_ajax() and request.GET['reqid']:
    if is_ajax:
        print("entered")
        reqid=request.GET['reqid']
        obj = Tbldocrequest.objects.get(pk=reqid)
        obj.doc_response = 1
        obj.save()
        return HttpResponse(1)

@api_view(['GET','PUT','POST'])
def decryptfile(request):
    is_ajax = request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"  
    #if is_ajax:

    #if request.is_ajax() and request.GET['docid']:
    if is_ajax:
        print("entered")
        print("decrypt")
        docid=request.GET['id']
        
        print(docid)
        obj=Tbldocument.objects.get(pk=docid)
        key=obj.encription_key
        encripted_key = key[1:]
        filename = "C:/securesystem/media/"+str(obj.filename)
        decrypt(filename,encripted_key)
        print(encripted_key)

        return Response({"data":"data"})

@api_view(['GET','PUT','POST'])
def encryptfile(request):
    is_ajax = request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"  
    #if is_ajax:

    #if request.is_ajax() and request.GET['docid']:
    if is_ajax:
        print("entered")
        docid=request.GET['id']
        
        print(docid)
        obj=Tbldocument.objects.get(pk=docid)
        key=obj.encription_key
        encripted_key = key[1:]
        filename = "C:/securesystem/media/"+str(obj.filename)
        encrypt(filename,encripted_key)
        print(encripted_key)

        return Response({"data":"data"})

