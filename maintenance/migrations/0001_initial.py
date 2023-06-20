# Generated by Django 4.2.2 on 2023-06-20 10:20

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vin_code', models.CharField(max_length=17, unique=True, validators=[django.core.validators.RegexValidator(regex='^[a-zA-Z0-9]{9}[a-zA-Z0-9-]{2}[0-9]{6}')], verbose_name='VIN')),
                ('vehicle_manufacturer', models.CharField(max_length=50, verbose_name='Manufacturer')),
                ('vehicle_model', models.CharField(max_length=20, verbose_name='Model')),
                ('vehicle_body', models.CharField(max_length=10, verbose_name='Body')),
                ('vehicle_year', models.IntegerField(verbose_name='Year')),
                ('vehicle_mileage', models.IntegerField(verbose_name='Mileage')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkPattern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('interval_month', models.IntegerField(blank=True, null=True, verbose_name='Interval in month')),
                ('interval_km', models.IntegerField(blank=True, null=True, verbose_name='Interval in kilometers')),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_type', models.CharField(choices=[('REPAIR', 'Repair'), ('MAINTENANCE', 'Maintenance'), ('TUNING', 'Tuning')], default='MAINTENANCE', max_length=20, verbose_name='Work Type')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('interval_month', models.IntegerField(blank=True, null=True, verbose_name='Interval in month')),
                ('interval_km', models.IntegerField(blank=True, null=True, verbose_name='Interval in kilometers')),
                ('note', models.CharField(blank=True, max_length=255, verbose_name='Note')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='works_list', to='maintenance.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='MileageEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mileage_date', models.DateField(verbose_name='Mileage Date')),
                ('mileage', models.IntegerField(verbose_name='Mileage')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mileage_events', to='maintenance.vehicle', verbose_name='Vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_date', models.DateField(verbose_name='Event Date')),
                ('mileage', models.IntegerField(verbose_name='Mileage')),
                ('part_price', models.FloatField(default=0.0, verbose_name='Part price')),
                ('work_price', models.FloatField(default=0.0, verbose_name='Work price')),
                ('note', models.CharField(blank=True, max_length=255, verbose_name='Note')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='maintenance.vehicle', verbose_name='Vehicle')),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work', to='maintenance.work', verbose_name='Work title')),
            ],
            options={
                'ordering': ['-work_date'],
            },
        ),
    ]