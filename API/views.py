from datetime import datetime,timedelta
import pytz
from math import inf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db.models import Q

from .forms import NewUserForm
from .serializers import CountrySerializer, GameSerializer, UserSerializer, PredictionSerializer, BracketPredictionSerializer
from bracket.models import Country, Game, Prediction, BracketPrediction, GroupError


class UsersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer = UserSerializer

    def get(self, request):
        """list users"""
        users = User.objects.filter(~Q(username__in = ["admin","JP"])).order_by('-points__points')
        serialized_users = self.serializer(users, many=True).data

        pos = 0 
        cur_points = inf
        for n,s_user in enumerate(serialized_users):
            if s_user["points"] < cur_points:
                pos += 1
                cur_points = s_user["points"] 
                s_user["rank"] = pos
            else:
                s_user["rank"] = ""            

        return Response(data=serialized_users, status=status.HTTP_200_OK)


class GamesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer = GameSerializer

    def get(self, request):
        """list games"""

        tz = pytz.timezone('America/Bogota')
        future_games = Game.objects.filter(game_date__gt = datetime.now(tz).date()+timedelta(days=1))
        today_games = Game.objects.filter(game_date= datetime.now(tz).date()+timedelta(days=1))


        serialized_future_games = self.serializer(future_games, many=True).data
        serialized_today_games = self.serializer(today_games, many=True).data
        data_out = {
            "p_future":serialized_future_games,
            "p_today":serialized_today_games
        }
        return Response(data=data_out, status=status.HTTP_200_OK)


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
    def get(self,request,*args,**kwargs):
        return redirect("/clasificatoria")

class PredictionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer = PredictionSerializer 

    def get(self, request, user_name=None):
        """Get predictions from one user"""
        user_name = user_name if user_name else request.user
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
    messages.error(request, "No se aceptan nuevos jugadores. \n Contacta con un administrador si queres ingresar.")
    return redirect("id:id")

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
