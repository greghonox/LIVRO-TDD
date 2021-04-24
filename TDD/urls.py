from lists import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^lists/new$', views.new_list, name='new_list'),
    url(r'^lists/the-only-list-in-the-wold/$', views.view_list, name='view_list'),
]
