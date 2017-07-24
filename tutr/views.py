from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def tutr_update(request):
	return render(request,'update.html',{})

def tutr_create(request):
    return HttpResponse("<h1> Create </h1>")
