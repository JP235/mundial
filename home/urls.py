from django.urls import path
from . import views
from django.views.generic import TemplateView
from bracket import views as br_views

app_name='home'
urlpatterns = [
    path('', views.LandingView.as_view(),name="home"),
    path('reglas', TemplateView.as_view(template_name="main/rules.html"),name="rules"),
    path('mis_predicciones', br_views.PredListView.as_view(), name='my_predictions'),
    path('predicciones/<str:username>', br_views.PredListView.as_view(), name='predictions_by_user'),
    path('partido/<int:game_id>', br_views.GameView.as_view(), name='game_by_id'),
    
    
]