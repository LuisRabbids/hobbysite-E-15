from django.shortcuts import render
from .models import Commissions
from django.http import HttpResponse

def index(request):
    return HttpResponse('Hellow World! This came from the index view')

def commissions_list(request):
    return 