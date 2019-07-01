from url_shortener import views
from django.conf.urls import url
from django.conf.urls import handler404, handler500

app_name = "url_shortener"
urlpatterns = [
    url(r'^$', views.submit_url, name='home'),
    url(r'^register/$', views.register, name="register"),
    url(r'^sign_in/$', views.sign_in, name='sign_in'),
    url(r"^sign_out/$", views.sign_out, name="sign_out"),
    url(r'^delete_url/', views.delete_url, name="delete_url"),
    url(r'^[A-Z][0-9][A-Za-z0-9]+/$', views.url_mapper, name="url_mapper"),
    url(r'^[a-zA-Z0-9]+/$', views.url_mapper, name="url_mapper"),
]
