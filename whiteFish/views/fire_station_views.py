import csv
import threading

import osmnx as ox
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect

from whiteFish.forms import FireStationForm
from whiteFish.geoLocate import get_shortest_distance, visualize_graph
from whiteFish.models import FireStation, BackgroundTask, Home, Distance, OutputFile
from whiteFish.views.home_views import any_tasks_running


@login_required
def home_action(request):
    form = FireStationForm()
    return render(request, 'whiteFish/fire_stations_index.html', {'items': get_fire_stations(),
                                                                  'form': form,
                                                                  'tasks': BackgroundTask.objects.filter(is_done=False),
                                                                  'error': BackgroundTask.objects.filter(is_done=True)
                                                                  })


@login_required
def add_action(request):
    form = FireStationForm()
    context = {'items': get_fire_stations(),
               'form': form,
               'tasks': BackgroundTask.objects.filter(is_done=False),
               'error': BackgroundTask.objects.filter(is_done=True)}

    form = FireStationForm(request.POST)
    if form.is_valid():
        data = form.clean()
        new_item = FireStation(name=data['name'], address=data['address'], cords_lat=data['cords_lat'],
                               cords_long=data['cords_long'])
        new_item.save()
        return redirect('fire-stations')
    else:
        context['error'] = form.errors
        return render(request, 'whiteFish/fire_stations_index.html', context)


@login_required
def delete_action(request, item_id):
    context = {'items': get_fire_stations()}

    if request.method != 'POST':
        context['error'] = 'Deletes must be done using the POST method'
        return render(request, 'whiteFish/fire_stations_index.html', context)

    try:
        delete_fire_stations_by_id(item_id)
        return redirect('fire-stations')
    except ObjectDoesNotExist:
        context['error'] = 'The item did not exist in the list'
        return render(request, 'whiteFish/fire_stations_index.html', context)


@login_required
def process_data_action(request):
    if request.method != 'POST':
        return redirect('fire-stations')

    if any_tasks_running():
        context = {'items': get_fire_stations(), 'form': FireStationForm(),
                   'tasks': BackgroundTask.objects.filter(is_done=False),
                   'error': 'Please wait for the current task to finish.'}
        return render(request, 'whiteFish/fire_stations_index.html', context)

    BackgroundTask.objects.all().delete()
    task = BackgroundTask()
    task.message = 'Processing Data'
    task.save()
    t = threading.Thread(target=process_data, args=(task.id,), daemon=True)
    t.start()
    return redirect('fire-stations')


def process_data(task_id):
    task = BackgroundTask.objects.get(id=task_id)
    try:
        ox.config(use_cache=True)
        G = ox.graph_from_place('Flathead County, Montana, USA', network_type='drive')
        visualize_graph('templates/whiteFish/flathead_county.html')
        task.message = 'Processing Data: 0%'
        task.save()
        i = 1
        j = Home.objects.count()
        k = FireStation.objects.count()
        Distance.objects.all().delete()
        for station in FireStation.objects.all():
            for home in Home.objects.all():
                distance = Distance()
                distance.fire_station = station
                distance.home = home
                distance.distance = get_shortest_distance(G,
                                                          (station.cords_lat, station.cords_long),
                                                          (home.cords_lat, home.cords_long))
                distance.save()
                task.message = 'Processing Data: ' + \
                               str(round((i / (j * k)) * 100, 2)) + '%'
                task.save()
                print(task.message)
                i += 1

        task.message = 'Processing Data: 100%'
        task.save()
        output_file = OutputFile()
        task.message = 'Writing Output File'
        task.save()
        output_file.file.save('distance-matrix.csv', ContentFile(''))
        path = output_file.file.path
        row_1 = [''] * 27 + ['{}'.format(i + 1) for i in range(len(FireStation.objects.all()))]
        row_2 = [''] * 27 + [fire_station.address for fire_station in FireStation.objects.all()]
        row_3 = [''] * 27 + [fire_station.name for fire_station in FireStation.objects.all()]
        home_fields = [field.name for field in Home._meta.fields]
        row_4 = ['id'] + home_fields[1:24] + [''] + ['Geocode', 'property_location'] + \
                ['{},{}'.format(fire_station.cords_lat, fire_station.cords_long)
                 for fire_station in FireStation.objects.all()]
        with open(path, 'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(row_1)
            write.writerow(row_2)
            write.writerow(row_3)
            write.writerow(row_4)

            for i, home in enumerate(Home.objects.all()):
                row = [i + 1]
                row += [getattr(home, field) for field in home_fields[1:24]]
                row += ['']
                row += ['{},{}'.format(home.cords_lat, home.cords_long), home.property_location]
                for station in FireStation.objects.all():
                    distance = Distance.objects.get(home=home, fire_station=station)
                    row += [distance.distance]
                write.writerow(row)
        task.delete()
    except Exception as e:
        task.is_done = True
        task.message = 'Error: ' + str(e)
        task.save()


def get_fire_stations():
    fire_stations = FireStation.objects.all()
    for i, fire_station in enumerate(fire_stations):
        fire_station.id = i + 1

    return fire_stations


def delete_fire_stations_by_id(fires_stations_id):
    FireStation.objects.all()[fires_stations_id - 1].delete()
