from django.shortcuts import render 
from django.http import HttpResponse 

# Create your views here.

def home(request):
    return HttpResponse("Welcome To the task managment system")

def contact(request):
    return HttpResponse("<h1 style = 'color: red'>This is Contact Page</h1>")

def show_task(request):
    return HttpResponse("This is our task Desk")
