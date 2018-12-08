from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect

def redirect_view(request):
    return redirect('/admin/core/movie/')
