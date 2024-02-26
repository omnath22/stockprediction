from . import views
from django.urls import path

urlpatterns = [
    path('', views.home),
    path('details',views.details),
    path('signout',views.signout)
]
