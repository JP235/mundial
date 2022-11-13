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

    def get(self,request):
        """list users"""
        
        users = User.objects.all()
        serialized_users = self.serializer(users, many=True).data
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
    serializer = PredictionSerializer

    def get(self,request, id: int = None):
        """Get predictions from one user"""
        if id:
            pred = Prediction.objects.get(pk = id)
            pred_serial = self.serializer(pred).data
        else:
            pred = Prediction.objects.filter(owner = request.user)
            pred_serial = self.serializer(pred, many=True).data
        
        return Response(data=pred_serial,status=status.HTTP_200_OK)  
    
    def post(self,request):
        """Make new prediction"""
        prediction_serial = self.serializer(request.data)

        if prediction_serial.is_valid():
            pred = prediction_serial.save()
            return Response(data=pred.data, status=status.HTTP_200_OK) 
        return Response(prediction_serial.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        """Change prediction"""
        old_prediction = Prediction.objects.get(pk = id)
        prediction_serial = self.serializer(old_prediction,request.data)

        if prediction_serial.is_valid():
            prediction_serial.save()
            return Response(data=prediction_serial.data,status=status.HTTP_200_OK)  
        return Response(prediction_serial.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        """Delete Prediction"""
        old_prediction = Prediction.objects.get(pk = id)
        old_prediction.delete()
        return Response(
        {'message': 'Prediction was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

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
