from django.urls import path
from . import views

app_name='API'
urlpatterns = [
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("games", views.GamesAPIView.as_view(), name="games" ),
    path("users", views.UsersAPIView.as_view(), name="users" ),
    path("predictions/", views.PredictionAPIView.as_view(), name="prediction" ), 
    path("predictions/<str:user_name>/", views.PredictionAPIView.as_view(), name="prediction_by_username" ),
    path("predict/<int:game_id>/", views.PredictionAPIView.as_view(), name="prediction_by_id" ),
    path("game_predictions/<int:game_id>", views.GamePredictionsAPIView.as_view(),name="predictions_by_game")
]