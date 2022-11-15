from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.http import urlencode
from django.shortcuts import render, redirect, get_object_or_404

from .models import Game, Prediction

number_to_fase = {
    0: "Grupos",
    1: "Fase de 16",
    2: "Cuartos de Final",
    3: "Semi-Final",
    4: "Final",
}


class GameView(ListView):
    """"""

    model = Game
    template_name = "bracket/game_page.html"

    def get(self, request, game_id):
        if len(game := Game.objects.filter(id=game_id)) > 0:
            game = game[0] 
            ctx = {
                "id": game.id,
                "fase": number_to_fase[game.wc_round],
                "team_1": game.team_1,
                "team_2": game.team_2,
            }
            return render(request, self.template_name, ctx)
        return redirect("home:my_predictions")


class PredListView(ListView):
    """"""
    model = Prediction
    template_name: str = "bracket/prediction_list.html"

    def get(self,request,username = None):
        ctx = {
        "username":username if username else request.user
        }
        return render(request,self.template_name,ctx)