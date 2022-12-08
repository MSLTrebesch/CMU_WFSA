"""whiteFish URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from whiteFish.views import fire_station_views, home_views, views, result_views, map_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.global_action, name='global'),
    # path('process', views.process_action, name='process'),
    # path('add_data', views.add_data_action, name='add_data'),
    # path('add_fire_station', views.add_fire_station_action, name='add_fire_station'),
    # path('whiteFish/out.csv', views.download_file),

    path('fire-stations', fire_station_views.home_action, name='fire-stations'),
    path('add-fire-station', fire_station_views.add_action, name='add-fire-station'),
    path('delete-fire-station/<int:item_id>', fire_station_views.delete_action, name='delete-fire-station'),
    path('process-data', fire_station_views.process_data_action, name='process-data'),

    path('homes', home_views.home_action, name='homes'),
    path('add-home', home_views.add_action, name='add-home'),
    path('delete-home/<int:item_id>', home_views.delete_action, name='delete-home'),

    path('result', result_views.home_action, name='result'),
    path('download/<int:item_id>', result_views.download_action, name='download'),

    path('density-map', map_views.density_map_action, name='density-map'),

    path('accounts/', include('django.contrib.auth.urls')),
]
