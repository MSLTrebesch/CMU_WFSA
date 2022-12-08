import mimetypes

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from whiteFish.geoLocate import geocode_address


@login_required
def global_action(request):
    return redirect('fire-stations')
