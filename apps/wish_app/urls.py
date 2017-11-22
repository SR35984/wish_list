from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="landing"),
    url(r'^register$', views.register, name="register"),
    url(r'^login$', views.login, name="login"),
    url(r'^dashboard$', views.dashboard, name="dashboard"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^wish_items/create$', views.create, name="create_item"),
    url(r'^addwish/(?P<item_id>[0-9]+)$', views.add_wish, name="add_wish"),
    url(r'^removewish/(?P<item_id>[0-9]+)$', views.remove_wish, name="remove_wish"),
    url(r'^wish_items/(?P<item_id>[0-9]+)$', views.show_item, name="show"),
    url(r'^delete/(?P<item_id>[0-9]+)$', views.delete, name="delete")
]