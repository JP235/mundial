from django.urls import path
from . import views
from django.views.generic import TemplateView
from bracket import views as br_views

app_name='home'
urlpatterns = [
    path('', views.LandingView.as_view(),name="home"),
    
]