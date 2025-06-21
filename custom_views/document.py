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
import os
import cryptography
from cryptography.fernet import Fernet

@api_view(['GET','POST'])
def doc_create(request):
	if request.method=='GET':
		return Response({'data':'','module':'Category'},template_name='ERP/document/create_update.html')
	else:
		filename=""
		getfile = request.FILES.get("filename")
		split_tup = os.path.splitext(str(getfile))
		file_name = split_tup[0]
		print("fil")
		print(file_name)
		serializer=TbldocumentSerializer(data=request.data)
		
		if serializer.is_valid():
			fileserializer=serializer.save()
			fileid = fileserializer.id
			obj = Tbldocument.objects.get(id=fileid)
			write_key()
			key = load_key()
			print("key")
			print(key)
			obj.encription_key = key
			obj.save()
			filename = "C:/securesystem/media/"+str(obj.filename)
			encrypt(filename, key)
			
			if request.accepted_renderer.format=='html':
				return Response({"success_data": "Data added successfully",'module':'document'},template_name='ERP/document/create_update.html')
			return Response({"data": "Data added successfully",'module':'document'},status=status.HTTP_201_CREATED)
		else:
			error_details = []
			for key in serializer.errors.keys():
				error_details.append({"field": key, "message": serializer.errors[key][0]})
			data = {
				"Error": {
				"status": 400,
				"message": "Your submitted data was not valid - please correct the below errors",
				"error_details": error_details
				}
				}
			if request.accepted_renderer.format=='html':
				return Response({"error_data": data},template_name='ERP/document/create_update.html')
			return Response(data, status=status.HTTP_400_BAD_REQUEST)

def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()

    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    return open("key.key", "rb").read()

def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    print("filename")
    
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

    print(file)

    return file

@api_view(['GET','PUT','POST'])
def list_doc(request):
	custom_filter={}
	custom_filter['deleted']=0

	obj = Tbldocument.objects.filter(**custom_filter)
	data = TbldocumentSerializer(obj, many=True).data
	if request.accepted_renderer.format == 'html':
		return Response({"data": data},template_name='ERP/document/list.html')
	return Response({"data": data})

@api_view(['GET','PUT','POST'])
def list_perm(request):
	custom_filter={}
	custom_filter['deleted']=0

	obj = Tblaccess.objects.filter(**custom_filter)
	data = TblaccessSerializer(obj, many=True).data
	if request.accepted_renderer.format == 'html':
		return Response({"data": data},template_name='ERP/document/perm_list.html')
	return Response({"data": data})


@api_view(['GET','POST'])
def access_permission(request):
    #project_obj = file.objects.get(pk=id)
    #data = fileSerializer(project_obj).data    
    if request.method=='GET':
        return Response({'data':"data",'module':'access_permission'},template_name='ERP/document/access_perm.html')
    else:
        serializer=TblaccessSerializer(data=request.data)
        if serializer.is_valid():
            qserializer=serializer.save()
        if request.accepted_renderer.format == 'html':
            return Response({"data": "data"},template_name='ERP/document/access_perm.html')
        return Response({"data": "data"},template_name='ERP/document/access_perm.html')

@api_view(['GET','PUT','POST'])
def doc_view(request,id):
    custom_filter={}
    custom_filter['deleted']=0

    project_obj = Tbldocument.objects.get(pk=id)
    project_data = TbldocumentSerializer(project_obj).data
    print(project_obj.filename)
    file = str(project_obj.filename)
    encripted_key = project_obj.encription_key
    encripted_key = encripted_key[1:]
    file_path = "C:/securesystem/media/"+file

    with open(file_path, "rb") as file:
        # read all file data
        file_data = file.read()

    if request.accepted_renderer.format == 'html':
        return Response({"data": file_data,'id':project_obj.id},template_name='ERP/document/doc_view.html')
    return Response({"data": file_data})


@api_view(['GET','PUT','POST'])
def encryptfile(request):
    if request.is_ajax() and request.GET['id']:
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

@api_view(['GET','POST'])
def get_rolename(request):
    if request.method=='GET':
        print("get")
        id = request.GET['id']
        print(id)
        custom_filter={}
        custom_filter['deleted']=0

        obj = Tblprofile.objects.get(user_id=id)
        #data = TblprofileSerializer(obj).data

        print("role")
        print(obj.role)
        role = obj.role
        name = ""
        if (role == "1"):
            name = "Managing Director"
        elif(role == "2"):
            name = "Team Leader"
        elif(role == "3"):
            name = "Developer"
        elif(role == "4"):
            name = "Clients"
        print("name")
        return Response({'data':"data","name":name,"role":role},template_name='ERP/document/access_perm.html')
    
    