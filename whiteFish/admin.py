from django.contrib import admin

from .models import FireStation, Home, Distance, InputFile, OutputFile, BackgroundTask

admin.site.register(FireStation)
admin.site.register(Home)
admin.site.register(Distance)
admin.site.register(InputFile)
admin.site.register(OutputFile)
admin.site.register(BackgroundTask)