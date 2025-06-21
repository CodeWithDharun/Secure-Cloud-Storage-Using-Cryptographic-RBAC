from rest_framework import serializers
from ERP.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class TblprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblprofile
        fields = "__all__"

class TbldocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbldocument
        fields = "__all__"

class TblaccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblaccess
        fields = "__all__"

class TbldocrequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbldocrequest
        fields = "__all__"