from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User

from .forms import NewUserForm, PredictionForm
from .serializers import GameSerializer, UserSerializer, PredictionSerializer
from bracket.models import Game, UsersPoints, Prediction


class UsersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer = UserSerializer

    def get(self, request):
        """list users"""

        users = User.objects.all()
        serialized_users = self.serializer(users, many=True).data
        return Response(data=serialized_users, status=status.HTTP_200_OK)


class GamesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer = GameSerializer

    def get(self, request):
        """list games"""
        games = Game.objects.all()
        serialized_games = self.serializer(games, many=True).data
        return Response(data=serialized_games, status=status.HTTP_200_OK)


class GamePredictionsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer = PredictionSerializer

    def get(self, request, game_id):
        game_predictions = Prediction.objects.filter(game=game_id)
        game_predictions_serial = self.serializer(game_predictions, many=True).data
        return Response(data=game_predictions_serial, status=status.HTTP_200_OK)


class PredictionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer = PredictionSerializer

    def get(self, request, userid=None):
        """Get predictions from one user"""
        pred_user = userid if userid else request.user
        print(request)
        pred = Prediction.objects.filter(owner=pred_user)
        pred_serial = self.serializer(pred, many=True).data
        return Response(data=pred_serial, status=status.HTTP_200_OK)

    def post(self, request, game_id):
        """Make new prediction"""

        if len(p := Prediction.objects.filter(owner=request.user.id, game=game_id)) > 0:
            print(p)
            return self.put(request, p[0].pk, to_predictions=False)

        new_prediction = Prediction.format_prediction_dict(request, game_id)
        prediction_serial = self.serializer(data=new_prediction)

        if prediction_serial.is_valid():
            prediction_serial.save()
            if next_url := request.POST.get("next"):
                return redirect(next_url)
            return redirect(f"/partido/{game_id+1}")

        return Response(prediction_serial.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pred_id, to_predictions=True):
        """Change prediction"""
        old_prediction = Prediction.objects.get(id=pred_id)
        prediction_serial = self.serializer(
            old_prediction,
            Prediction.format_prediction_dict(request, old_prediction.game.pk),
        )

        if prediction_serial.is_valid():
            prediction_serial.save()
            print("")
            print("request")
            print(request.POST)
            print("")
            if next_url := request.POST.get("next"):
                return redirect(next_url)
            if to_predictions:
                return redirect(f"/mis_predicciones")
            return redirect(f"/partido/{old_prediction.game.pk+1}")


def login_request(request):
    if request.user.is_authenticated:
        return redirect("home:home")
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("home:home")
    messages.error(request, "Informacion Incorrecta.")
    return redirect("id:id")


def register_request(request):
    if request.user.is_authenticated:
        return redirect("home:home")
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home:home")
    messages.error(request, "Informacion Incorrecta.")
    return redirect("id:id")
