from django.urls import path
from . import views

app_name='bracket'
urlpatterns = [
  path('partido/<int:id>', views.GameView.as_view(), name='game_by_id'),
#   path('partidos', views.GameView.as_view(), name='game'),
  path('predicciones', views.PredListView.as_view(), name="predictions")

]