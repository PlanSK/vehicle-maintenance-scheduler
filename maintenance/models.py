from django.db import models


class Vehicle(models.Model):
    vin_code = models.CharField(max_length=17, verbose_name='VIN')
    vehicle_manufacturer = models.CharField(max_length=50,
                                            verbose_name='Manufacturer')
    vehicle_model = models.CharField(max_length=20, verbose_name='Model')
    vehicle_body = models.CharField(max_length=10, verbose_name='Body')
    vehicle_year = models.IntegerField(verbose_name='Year')
    vehicle_mileage = models.IntegerField(verbose_name='Mileage')

    def __str__(self):
        return ' '.join((self.vehicle_manufacturer, self.vehicle_model,
                         self.vehicle_body, str(self.vehicle_year)))

    def save(self, *args, **kwargs):
        self.vin_code = self.vin_code.upper()
        super().save(*args, **kwargs)


class Work(models.Model):
    class WorkType(models.TextChoices):
        REPAIR = 'REPAIR', 'Repair'
        MAINTENANCE = 'MAINTENANCE', 'Maintenance'
        TUNING = 'TUNING', 'Tuning'

    work_type = models.CharField(
        max_length=20, choices=WorkType.choices, default=WorkType.MAINTENANCE,
        verbose_name='Work Type')
    title = models.CharField(max_length=255, verbose_name='Title')
    interval_month = models.IntegerField(verbose_name='Interval in month')
    interval_km = models.IntegerField(verbose_name='Interval in kilometers')


class Event(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE,
                                related_name='events', verbose_name='Vehicle')
    work_date = models.DateField(verbose_name='Event Date')
    mileage = models.IntegerField(verbose_name='Mileage')
    work = models.ForeignKey(Work, on_delete=models.PROTECT,
                             related_name='work', verbose_name='Work title')
    part_price = models.FloatField(verbose_name='Part price', default=0.0)
    work_price = models.FloatField(verbose_name='Work price', default=0.0)
    note = models.CharField(max_length=255, verbose_name='Note')


class MileageEvent(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE,
                                related_name='mileage_events',
                                verbose_name='Vehicle')
    mileage_date = models.DateField(verbose_name='Mileage Date')
    mileage = models.IntegerField(verbose_name='Mileage')
