
from django.conf.urls import include, url
import views as jasmine_views

urlpatterns = [
    url(r'^$', jasmine_views.run_tests, name='run_tests')
]
