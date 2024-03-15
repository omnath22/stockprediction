from . import views
from django.urls import path

urlpatterns = [
    path('',views.home),
    path('index', views.home),
    path('subscribe',views.subscribe),
    path('details',views.details),
    path('disclaimer',views.disclaimer),
    path('signout',views.signout),
    path('chat/', views.chat_view, name='chat'),
    path('watchlist',views.watchlist),
    path('selectPlan',views.selectPlan),
]
