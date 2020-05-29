from django.conf.urls import url
from django.urls import path
from . import views

app_name = "resource"
urlpatterns = [
    path('upload', views.upload),
    path('personal', views.personal),
    url('detail1/(?P<pk>\d+)', views.detail1, name="detail1"),
    url('photo/(?P<user_id>\d+)', views.photo, name="photo"),
    url('download/(?P<id>\d+)', views.download, name="download"),
    path('comment', views.comments, name="comment"),
]
