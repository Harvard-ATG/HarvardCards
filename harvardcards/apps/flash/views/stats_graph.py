from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.forms import widgets

from harvardcards.apps.flash.models import Collection, Deck, Card, Decks_Cards, Users_Collections, User
from harvardcards.apps.flash.forms import DeckImportForm
from harvardcards.apps.flash.decorators import check_role
from harvardcards.apps.flash.lti_service import LTIService
from harvardcards.apps.flash import services, queries, analytics
from django.contrib.auth.decorators import user_passes_test

import PIL
import PIL.Image
import StringIO
from matplotlib import pylab
from pylab import *
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def initialize_graph():
    close('all')
    fig=Figure(facecolor='#f3f3f1')
    ax=fig.add_subplot(111)
    ax.tick_params(axis="both", which="both", bottom="on", top="off",pad=5,
                    labelbottom="on", left="on", right="off", labelleft="on", direction='out')
    return [fig, ax]


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def graph_collections(request):
    objects = Users_Collections.objects.all().values()
    objects = map(lambda o: o['user_id'], objects)
    users = User.objects.all().values_list('id', flat=True)
    x = map(lambda u: objects.count(u), users)


    [fig, ax] = initialize_graph()
    ax.patch.set_facecolor('#f5f5f5')
    n, bins, patches = ax.hist(x, facecolor='#A51C30', alpha=0.75)
    ax.set_ylim((0, max(n)+4))
    ax.set_xlabel('Number of Collections')
    ax.set_ylabel('Number of Users')
    ax.set_title('Histogram of Number of Viewable Collections Per User')

    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def graph_users(request):
    regs =  User.objects.all().values_list('date_joined', flat=True)
    min_date, max_date = min(regs).date(), max(regs).date()
    num_days = (max_date - min_date).days + 1
    date_list = [min_date + datetime.timedelta(days=x) for x in range(0, num_days)]
    x = map(lambda d: len(filter(lambda r: r.date() <= d, regs)), date_list)

    [fig, ax] = initialize_graph()
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d/%Y'))
    ax.xaxis.set_major_locator(matplotlib.dates.DayLocator(interval=len(x)/5))
    ax.patch.set_facecolor('#f5f5f5')
    ax.plot(date_list, x, color='#A51C30', linewidth=2)
    ax.set_ylabel('Number of Users')
    ax.set_title('Number of Registered Users Over Time')

    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def graphs(request):
    return render(request, 'stats_graphs.html')