from django.urls import path
from . import views

urlpatterns = [
    path('find/<pk>', views.find),
    path('del/<pk>', views.del_user),
    path('change/<pk>', views.change),
    path('photo', views.show_photo),
    path('friends', views.my_friends, name="friends"),
    path('change_new/<pk>', views.change_new),
]
