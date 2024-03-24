from service.models import *

def create_or_update_availability(provider_service, day, available, start_time, end_time):
    avail_instance, created = ProviderAvailability.objects.get_or_create(service=provider_service, day=day)
    avail_instance.day = day
    avail_instance.available = available
    avail_instance.start_time = start_time
    avail_instance.end_time = end_time
    avail_instance.save()
    return avail_instance, created