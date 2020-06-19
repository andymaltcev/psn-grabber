from django.shortcuts import render
from django.http import HttpResponse

def starting_view(request):
    return render(request,'pages/index.html')


# Create your views here.
