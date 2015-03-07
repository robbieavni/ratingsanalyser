from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import FormView


def index(request):
    return HttpResponse("Home Page")