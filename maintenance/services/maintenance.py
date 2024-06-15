from enum import Enum
from dataclasses import dataclass
import datetime

from dateutil.relativedelta import relativedelta

from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings

from maintenance.models import Work, Vehicle, Event


class WorkTrigger(Enum):
    NONE = 0
    MILEAGE = 1
    DATE = 2

class OutOfDateMileageLevel(Enum):
    FRESH = 0
    WARNING = 1
    OLD = 2

@dataclass
class PlanedWork:
    work: Work
    trigger: WorkTrigger
    planed_mileage: int
    mileage_delta: int
    planed_date: datetime.date | None
    date_delta: datetime.timedelta | None
    last_event_date: datetime.date
    remaining_procentage: int
    current_event_counter: int


def get_maintenance_limits(vin_code: str) -> list[PlanedWork]:
    current_vehicle = get_object_or_404(Vehicle, vin_code=vin_code)
    vehicle_events = current_vehicle.events.all()
    worklist = []
    limit_mileage = 0
    mileage_delta = 0
    mileage_remaining_procentage = 0
    limit_date = None
    date_delta = None

    for current_work in Work.objects.filter(
            vehicle__vin_code=vin_code,
            work_type=Work.WorkType.MAINTENANCE):
        current_event_list: Event = vehicle_events.filter(
            work=current_work).order_by('-work_date')
        current_event_counter = current_event_list.count()
        last_event = current_event_list.first()
        if not last_event:
            continue
        if current_work.interval_km:
            limit_mileage = last_event.mileage + current_work.interval_km
            mileage_delta = limit_mileage - current_vehicle.vehicle_mileage
            mileage_remaining_procentage = 100 - round(
                (mileage_delta / current_work.interval_km) * 100
            )
        if current_work.interval_month:
            limit_date = last_event.work_date + relativedelta(
                months=current_work.interval_month)
            date_delta = timezone.now().date() - limit_date

        if (current_work.interval_km
            and current_vehicle.vehicle_mileage >= limit_mileage):
            work_triger = WorkTrigger.MILEAGE
        elif (current_work.interval_month
              and timezone.now().date() >= limit_date):
            work_triger = WorkTrigger.DATE
        else:
            work_triger = WorkTrigger.NONE

        worklist.append(
            PlanedWork(
                work=current_work,
                trigger=work_triger,
                planed_mileage=limit_mileage,
                mileage_delta=mileage_delta,
                planed_date=limit_date,
                date_delta=date_delta,
                last_event_date=last_event.work_date,
                remaining_procentage=mileage_remaining_procentage,
                current_event_counter=current_event_counter
            )
        )

    return sorted(worklist, key=lambda work: work.last_event_date,
                  reverse=True)


def get_outdate_mileage_level(vin_code: str) -> int:
    current_date = timezone.now().date()
    current_vehicle = get_object_or_404(Vehicle, vin_code=vin_code)
    mileage_date_timedelta = (
        current_date - current_vehicle.vehicle_last_update_date
    ).days
    outofdate_level = OutOfDateMileageLevel.FRESH
    if (settings.WARNING_OUTDATE_LEVEL <= mileage_date_timedelta <
        settings.OLD_OUTDATE_LEVEL):
        outofdate_level = OutOfDateMileageLevel.WARNING
    elif mileage_date_timedelta >= settings.OLD_OUTDATE_LEVEL:
        outofdate_level = OutOfDateMileageLevel.OLD
    
    return outofdate_level.value


def get_average_mileage_interval(events_list: QuerySet) -> int:
    event_counter = events_list.count()
    previous_mileage = events_list.first().mileage
    mileage_delta_sum = 0
    if event_counter <= 1:
        return 0 
    for event in events_list:
        mileage_delta_sum += previous_mileage - event.mileage
        previous_mileage = event.mileage
    return mileage_delta_sum // (event_counter - 1)