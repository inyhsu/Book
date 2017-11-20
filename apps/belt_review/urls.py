from django.conf.urls import url
from . import views     

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^books$', views.books),
    url(r'^logout$', views.logout),
    url(r'^books/add$', views.books_add),
    url(r'^books/add_book$', views.add_book),
    url(r'^books/(?P<id>\d+)$', views.show_book),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^books/(?P<id>\d+)/create$', views.add_review),
    url(r'^users/(?P<id>\d+)$', views.show_user),

]