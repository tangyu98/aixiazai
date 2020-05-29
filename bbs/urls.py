from django.urls import path
from django.conf.urls import url
from . import views

app_name = "bbs"
urlpatterns = [
    url('^$', views.StudentList.as_view(), name='index'),
    path('detail/<int:pk>', views.StudentDetailView.as_view(), name="detail")
]
