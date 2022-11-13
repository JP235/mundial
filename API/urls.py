from django.urls import path
from . import views

app_name='API'
urlpatterns = [
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("games", views.GamesAPIView.as_view(), name="games" ),
    path("users", views.UsersAPIView.as_view(), name="users" ),
    path("predictions", views.PredictionAPIView.as_view(), name="prediction" ),
    path("prediction/<int:id>/", views.PredictionAPIView.as_view(), name="prediction_by_id" ),

    
]