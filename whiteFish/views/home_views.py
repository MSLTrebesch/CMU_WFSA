import csv
import threading

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from whiteFish.forms import UploadFileForm
from whiteFish.geoLocate import geocode_address
from whiteFish.models import Home, InputFile, BackgroundTask


@login_required
def home_action(request):
    form = UploadFileForm()
    return render(request, 'whiteFish/home_index.html', {'items': get_homes(),
                                                         'form': form,
                                                         'tasks': BackgroundTask.objects.filter(is_done=False),
                                                         'error': BackgroundTask.objects.filter(is_done=True)
                                                         })


@login_required
def add_action(request):
    form = UploadFileForm()
    context = {'items': get_homes(),
               'form': form,
               'tasks': BackgroundTask.objects.all(),
               'error': BackgroundTask.objects.filter(is_done=False)}

    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid() and not any_tasks_running():
        form.save()
        process_file()
        return redirect('homes')
    else:
        if any_tasks_running():
            context['error'] = 'Please wait for the current task to finish.'
        else:
            context['error'] = form.errors
        return render(request, 'whiteFish/home_index.html', context)


@login_required
def delete_action(request, item_id):
    context = {'items': Home.objects.all()}

    if request.method != 'POST':
        context['error'] = 'Deletes must be done using the POST method'
        return render(request, 'whiteFish/home_index.html', context)

    try:
        delete_home_by_id(item_id)
        return redirect('homes')
    except ObjectDoesNotExist:
        context['error'] = 'The item did not exist in the List.'
        return render(request, 'whiteFish/home_index.html', context)


def process_file():
    BackgroundTask.objects.all().delete()
    task = BackgroundTask()
    task.input = InputFile.objects.latest('id')
    task.message = 'Processing Input File'
    task.save()
    t = threading.Thread(target=geocode, args=(task.id,), daemon=True)
    t.start()


def geocode(task_id):
    task = BackgroundTask.objects.get(id=task_id)
    try:
        input_file = InputFile.objects.get(id=task.input.id)
        Home.objects.all().delete()
        with open(input_file.file.path, "r") as f:
            reader = csv.DictReader(f)
            # WFSA Tax	Market Value	Taxable Value	Type	Land Mkt	Land Taxable	Imp Market	Imp Taxable	PP Mkt	PP Taxable	Address	Assrno	City	Datestamp	ForCountry	State	Typ	Year	ZipcdWFSA Tax	Market Value	Taxable Value	Type	Land Mkt	Land Taxable	Imp Market	Imp Taxable	PP Mkt	PP Taxable	Address	Assrno	City	Datestamp	ForCountry	State	Typ	Year	Zipcd
            # Prior Year Fire Ambulance Fee	Total Market Value	Total Taxable Value	Type	Real Estate Market Value	Real Estate Taxable Value	Property Improvements Market Value	Property Improvements Taxable Value	PP Mkt	PP Taxable		Property Location	Assrno	City	Datestamp	ForCountry	State	Typ	Year	Zipcd
            for row in reader:
                home = Home()
                home.year = row['Year'].strip()
                home.sd = row['SD'].strip()
                home.assessor_number = row['Assr'].strip()
                home.owner_of_record = row['Owner'].strip()
                home.tax_bill = row['Taxbill'].strip()
                home.res_units = row['Res Units'].strip()
                home.comm_units = row['Comm Units'].strip()
                home.prior_year_fire_ambulance_fee = row['WFSA Tax'].strip()
                home.total_market_value = row['Market Value'].strip()
                home.total_taxable_value = row['Taxable Value'].strip()
                home.type = row['Type'].strip()
                home.real_estate_market_value = row['Land Mkt'].strip()
                home.real_estate_taxable_value = row['Land Taxable'].strip()
                home.property_improvements_market_value = row['Imp Market'].strip()
                home.property_improvements_taxable_value = row['Imp Taxable'].strip()
                home.pp_market_value = row['PP Mkt'].strip()
                home.pp_taxable_value = row['PP Taxable'].strip()
                home.property_location = row['Address'].strip()
                home.city = row['City'].strip()
                home.state = row['State'].strip()
                home.zip_code = row['Zipcd'].strip()
                address = home.property_location + ', ' + home.city + ', ' + home.state + ' ' + str(home.zip_code)
                home.cords_lat, home.cords_long = geocode_address(address)
                home.save()
        task.delete()
    except Exception as e:
        task.message = 'Error: ' + str(e)
        task.is_done = True
        task.save()


def any_tasks_running():
    tasks = BackgroundTask.objects.all()
    for task in tasks:
        if not task.is_done:
            return True
    return False


def get_homes():
    homes = Home.objects.all()
    for i, home in enumerate(homes):
        home.id = i + 1

    return homes


def delete_home_by_id(home_id):
    Home.objects.all()[home_id - 1].delete()
