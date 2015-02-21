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
import numpy as np

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def graph_collections(request):
    objects = Users_Collections.objects.all().values()
    objects = map(lambda o: o['user_id'], objects)
    users = map(lambda u: u['id'], User.objects.all().values('id'))
    x = map(lambda u: objects.count(u), users)
    figure(facecolor='#f3f3f1')
    ax = gca()
    ax.patch.set_facecolor('#f5f5f5')
    n, bins, patches = hist(x, facecolor='#A51C30', alpha=0.75)
    ylim((0, max(n)+4))
    xlabel('Number of Collections')
    ylabel('Number of Users')
    title('Histogram of Number of Collections Associated with Users')
    tick_params(axis="both", which="both", bottom="on", top="off",pad=5,
                    labelbottom="on", left="on", right="off", labelleft="on", direction='out')

    buffer = StringIO.StringIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG = PIL.Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
    graphIMG.save(buffer, 'PNG')
    pylab.close()
    return HttpResponse(buffer.getvalue(), mimetype='img/png')


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def graphs(request):
    return render(request, 'stats_graphs.html')