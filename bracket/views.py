from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.http import urlencode
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .models import Game, Prediction, Country

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

    def get(self, request, username=None):
        ctx = {"username": username if username else request.user}
        return render(request, self.template_name, ctx)


class BracketView(View):
    context_object_name = 'ctx'

    def get(self, request):
        countries = Country.objects.all().order_by("group")
        ctx = {
            "A": countries[0:4],
            "B": countries[4:8],
            "C": countries[8:12],
            "D": countries[12:16],
            "E": countries[16:20],
            "F": countries[20:24],
            "G": countries[24:28],
            "H": countries[28:32],
        }
        return render(request, "bracket/grand_bracket_page.html",context=ctx)
