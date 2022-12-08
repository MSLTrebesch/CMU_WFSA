import mimetypes

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from whiteFish.models import OutputFile


@login_required
def home_action(request):
    return render(request, 'whiteFish/result_index.html', {'items': OutputFile.objects.all()})


@login_required
def download_action(request, item_id):
    item = OutputFile.objects.get(id=item_id)
    fl_path = item.file.path
    filename = item.file.name

    fl = open(fl_path, 'r')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
