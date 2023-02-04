from django.shortcuts import render
from base.models import *
from django.utils import timezone
import datetime
# Create your views here.
def home(request):
    context = {}
    event_dates = EventDates.objects.all().order_by('-event_start').first()
    # print(event_dates)
    current_time = timezone.now()
    time_diff = 0
    end = False
    if event_dates.event_start > current_time:
        # hunt is yet to begin
        time_diff = (event_dates.event_start - current_time).total_seconds()
        msg = "The Hunt begins in"
    elif event_dates.event_end > current_time:
        time_diff = (event_dates.event_end - current_time).total_seconds()
        msg = "The hunt ends in"
    else:
        time_diff = (event_dates.event_end - current_time).total_seconds()
        msg = "The Hunt has ended"
        end = True
    context['msg'] = msg
    context['time_diff'] = int(time_diff)
    context['has_ended'] = end
    print(context)
    return render(request,'base/home.html',context)