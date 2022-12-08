from django import forms

from whiteFish.geoLocate import geocode_address
from whiteFish.models import InputFile


class FireStationForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    address = forms.CharField(max_length=50, required=False)
    cords_lat = forms.FloatField(required=False)
    cords_long = forms.FloatField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        address = cleaned_data.get('address')
        cords_lat = cleaned_data.get('cords_lat')
        cords_long = cleaned_data.get('cords_long')
        if not (address or (cords_lat and cords_long)):
            raise forms.ValidationError('You must provide either an address or coordinates.')

        if address and not (cords_lat and cords_long):
            cleaned_data['cords_lat'], cleaned_data['cords_long'] = geocode_address(address)

        return cleaned_data


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = InputFile
        fields = ['file']
