from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from .forms import NewUserForm
from .serializers import CountrySerializer, GameSerializer, UserSerializer, PredictionSerializer, BracketPredictionSerializer
from bracket.models import Country, Game, Prediction, BracketPrediction, GroupError


class UsersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer = UserSerializer

    def get(self, request):
        """list users"""
        users = User.objects.all().order_by('-points__points')
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

class CountriesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer = CountrySerializer
    
    def get(self, request):
        """Get countries"""
        countries = Country.objects.all().order_by('group')
        countries_serial = self.serializer(countries, many=True).data
        return Response(data=countries_serial, status=status.HTTP_200_OK)
    

class BracketPredictionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer = BracketPredictionSerializer

    def post(self, request):
        """Make Bracket prediction"""
        
        try:
            new_prediction = BracketPrediction.format_request(request)
            prediction_serial = self.serializer(data=new_prediction)
            print(prediction_serial)
            if prediction_serial.is_valid():
                    prediction_serial.save()
        except GroupError as e:
            messages.error(request,e)
        except ValueError as e:
            messages.error(request,e)
        except ObjectDoesNotExist as e:
            messages.error(request,"No se pueden dejar opciones sin equipo elegido")

        return redirect("/clasificatoria")

class PredictionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer = PredictionSerializer 

    def get(self, request, user_name=None):
        """Get predictions from one user"""
        user_name = user_name if user_name else request.user
        print(user_name)
        pred = User.objects.get(username = user_name).predictions.order_by('game__game_date', 'game__game_time')
        pred_serial = self.serializer(pred, many=True).data
        return Response(data=pred_serial, status=status.HTTP_200_OK)

    def post(self, request, game_id):
        """Make new prediction"""

        if len(p := Prediction.objects.filter(owner=request.user.id, game=game_id)) > 0:
            return self.put(request, p[0].pk, to_predictions=False)

        new_prediction = Prediction.format_prediction_dict(request, game_id)
        prediction_serial = self.serializer(data=new_prediction)

        if prediction_serial.is_valid():
            prediction_serial.save()
            if next_url := request.POST.get("next"):
                return redirect(next_url)
            return redirect(f"/partido/{game_id+1}")
        
        messages.error("Informacion Erronea")
        return redirect(f"/partido/{game_id}")

    def put(self, request, pred_id, to_predictions=True):
        """Change prediction"""
        old_prediction = Prediction.objects.get(id=pred_id)
        prediction_serial = self.serializer(
            old_prediction,
            Prediction.format_prediction_dict(request, old_prediction.game.pk),
        )

        if prediction_serial.is_valid():
            prediction_serial.save()
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
        return redirect("home:landing")
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
            return redirect("home:landing")
    messages.error(request, "Informacion Incorrecta.")
    return redirect("id:id")
