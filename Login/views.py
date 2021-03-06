# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions
from models import User
from rest_framework.response import Response
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import smtplib
import requests
import json
from django.core.mail import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import base64
import struct
import hashlib
from django.views.decorators.csrf import csrf_exempt
from geopy.geocoders import Nominatim


# Create your views here.
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
# Checks user registration
def checkmatch(request):
    if request.method == 'POST':
        id = request.POST.get('email')
        pwd = request.POST.get('pass')
        try:
            checkuser = User.objects.get(email=id)
        except ObjectDoesNotExist:
            checkuser = None

        if checkuser is not None:
            if pwd == checkuser.password:
                response_data = {}
                response_data['id'] = checkuser.id
                response_data['email'] = checkuser.email
              #  print response_data
                return Response(response_data)
            else:
                return Response("nomatch")


        else:
            return Response("nouser")


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
#Matching of the hash generated from image with that of the hash provided from the server
def unhash(request):
    if request.method == 'POST':
        photo=request.POST.get('photo')
        hashcode=request.POST.get('hashcode')
        encrypted=request.POST.get('encrypted')

        image = open("image.jpeg", "wb")
        image.write(photo.decode('base64'))
        image.close()
        print(encrypted)

        data_base64 = photo # ANY STRING IN BASE64 FORMAT

        data_bytes = base64.decodestring(data_base64)  # CONVERTING THE BASE64 FORMAT TO DATA BYTES
        print(type(data_bytes))
        m = hashlib.md5()
        m.update(data_bytes)
        a=m.digest()
        b = (a.encode('base64'))


    return Response("matched")

#Splits the encrypted concatenated string to yield timestamp and coordinate details, further maps the coordinates to the location address.
def location(request):
    encrypted = "28.6644636_77.2321377_14_18_27_2_2018"
    list = encrypted.split("_")
    print list
    list.pop(2)
    list.pop(2)
    list.pop(2)
    list.pop(2)
    list.pop(2)
    geolocator = Nominatim()
    location = geolocator.reverse(list)
    print(location.address)
    #html = "<html><body>location.address</body></html>" 
    return HttpResponse("hello")




