from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def density_map_action(request):
    return render(request, 'whiteFish/flathead_county.html', {})
