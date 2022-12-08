from django.db import models


class FireStation(models.Model):
    """
    A model representing a fire station.
    """
    name = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    cords_lat = models.FloatField()
    cords_long = models.FloatField()

    def __str__(self):
        return self.address + '\t' + str(self.cords_lat) + '\t' + str(self.cords_long)


class Home(models.Model):
    """
    A model representing a home.
    """
    year = models.IntegerField(blank=True, null=True)
    sd = models.IntegerField(blank=True, null=True)
    assessor_number = models.CharField(max_length=50, blank=True, null=True)
    owner_of_record = models.CharField(max_length=50, blank=True, null=True)
    tax_bill = models.CharField(max_length=50, blank=True, null=True)
    res_units = models.IntegerField(blank=True, null=True)
    comm_units = models.IntegerField(blank=True, null=True)
    prior_year_fire_ambulance_fee = models.CharField(max_length=50, blank=True, null=True)
    total_market_value = models.CharField(max_length=50, blank=True, null=True)
    total_taxable_value = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    real_estate_market_value = models.CharField(max_length=50, blank=True, null=True)
    real_estate_taxable_value = models.CharField(max_length=50, blank=True, null=True)
    property_improvements_market_value = models.CharField(max_length=50, blank=True, null=True)
    property_improvements_taxable_value = models.CharField(max_length=50, blank=True, null=True)
    pp_mkt = models.CharField(max_length=50, blank=True, null=True)
    pp_tax = models.CharField(max_length=50, blank=True, null=True)
    property_location = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True, null=True)
    datestamp = models.DateTimeField(format('%Y%m%d'), blank=True, null=True)
    county = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)
    cords_lat = models.FloatField()
    cords_long = models.FloatField()

    def __str__(self):
        return self.property_location + '\t' + str(self.cords_lat) + '\t' + str(self.cords_long)


class Distance(models.Model):
    """
    A model representing the distance between a fire station and a home.
    """
    fire_station = models.ForeignKey(FireStation, on_delete=models.CASCADE)
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    distance = models.FloatField()

    def __str__(self):
        return str(self.fire_station) + '\t' + str(self.home) + '\t' + str(self.distance)


class InputFile(models.Model):
    """
    A model representing an input file.
    """
    file = models.FileField(upload_to='input_files')
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class OutputFile(models.Model):
    file = models.FileField(upload_to='output_files')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class BackgroundTask(models.Model):
    input = models.ForeignKey(InputFile, on_delete=models.CASCADE, null=True)
    output = models.ForeignKey(OutputFile, on_delete=models.CASCADE, null=True)
    is_done = models.BooleanField(default=False)
    message = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + '\t' + str(self.is_done) + '\t' + str(self.date_created)
