from enum import Enum
from dataclasses import dataclass
import datetime

from dateutil.relativedelta import relativedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone

from maintenance.models import Work, Vehicle, Event


class WorkTrigger(Enum):
    NONE = 0
    MILEAGE = 1
    DATE = 2

@dataclass
class PlanedWork:
    work: Work
    trigger: WorkTrigger
    planed_mileage: int
    mileage_delta: int
    planed_date: datetime.date
    date_delta: datetime.timedelta
    last_event_date: datetime.date
    remaining_procentage: int
    current_event_counter: int


def get_maintenance_limits(vin_code: str) -> list[PlanedWork]:
    current_vehicle = get_object_or_404(Vehicle, vin_code=vin_code)
    vehicle_events = current_vehicle.events.all()
    worklist = []

    for current_work in Work.objects.filter(
            vehicle__vin_code=vin_code,
            work_type=Work.WorkType.MAINTENANCE):
        current_event_list: Event = vehicle_events.filter(
            work=current_work).order_by('-work_date')
        current_event_counter = current_event_list.count()
        last_event = current_event_list.first()
        if (not last_event or not current_work.interval_km
                and not current_work.interval_month):
            continue
        limit_mileage = last_event.mileage + current_work.interval_km
        mileage_delta=limit_mileage - current_vehicle.vehicle_mileage
        mileage_remaining_procentage = 100 - round(
            (mileage_delta / current_work.interval_km) * 100
        )
        limit_date = last_event.work_date + relativedelta(
            months=current_work.interval_month)
        if current_vehicle.vehicle_mileage >= limit_mileage:
            work_triger = WorkTrigger.MILEAGE
        elif timezone.now().date() >= limit_date:
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
                date_delta=timezone.now().date() - limit_date,
                last_event_date=last_event.work_date,
                remaining_procentage=mileage_remaining_procentage,
                current_event_counter = current_event_counter
            )
        )

    return sorted(worklist, key=lambda work: work.last_event_date,
                  reverse=True)
