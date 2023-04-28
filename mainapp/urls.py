from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login_ ,name= "login"),
    path('signup/', views.signup_ ,name= "signup"),
    path('logout/',views.logout_, name= "logout"),
    # path('get', views.setTable , name = "get"),
]
