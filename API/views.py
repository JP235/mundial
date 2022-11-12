from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User

from .forms import NewUserForm
from .serializers import GameSerializer, UserSerializer
from bracket.models import Game, UsersPoints, Prediction


class UsersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer = UserSerializer

    def get(self,request):
        """list users"""
        
        print(request)
        print("")
        users = User.objects.all()
        print(users)
        serialized_users = self.serializer(users, many=True).data
        print("")
        print(serialized_users)
        print("")
        return Response(data=serialized_users,status=status.HTTP_200_OK)


class GamesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer = GameSerializer

    def get(self,request):
        """list games"""
        games = Game.objects.all()
        serialized_games = self.serializer(games, many=True).data
        return Response(data=serialized_games,status=status.HTTP_200_OK)

class PredictionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]


def login_request(request):
    if request.user.is_authenticated:
        return redirect("home:home")
    username = request.POST.get('username')
    password = request.POST.get('password')
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
