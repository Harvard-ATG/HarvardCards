from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from harvardcards.apps.flash.models import Collection, Users_Collections, User
import json
import calendar
import datetime

def get_graph_collections():
    objects = Users_Collections.objects.all().values()
    objects = map(lambda o: o['user_id'], objects)
    users = User.objects.all().values_list('id', flat=True)
    object_counts = map(lambda u: objects.count(u), users)

    raw_data = []
    for num_collections in sorted([x for x in set(object_counts)]):
        num_users = sum([1 for x in object_counts if x == num_collections])
        raw_data.append([num_collections, num_users])

    return raw_data

def get_graph_users():
    regs =  User.objects.all().values_list('date_joined', flat=True)
    min_date, max_date = min(regs).date(), max(regs).date()
    num_days = (max_date - min_date).days + 1
    date_list = [min_date + datetime.timedelta(days=x) for x in range(0, num_days)]
    x = map(lambda d: len(filter(lambda r: r.date() <= d, regs)), date_list)

    raw_data = []
    for idx, reg_date in enumerate(date_list):
        raw_data.append([calendar.timegm(reg_date.timetuple())*1000, x[idx]]) 

    return raw_data

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def graphs(request):
    context = {}
    context["graphs"] = {
        "userExperienceGraph": {"data": get_graph_collections()},
        "registrationGraph": {"data": get_graph_users()}
    }
    context['graphs'] = json.dumps(context['graphs'])
    return render(request, 'stats_graphs.html', context)
