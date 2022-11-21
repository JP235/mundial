from datetime import datetime
from typing import List
import pytz

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.http import urlencode
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q

from .models import Game, Prediction, Country, BracketPrediction

number_to_fase = {
    0: "Grupos",
    1: "Fase de 16",
    2: "Cuartos de Final",
    3: "Semi-Final",
    4: "Final",
}


class GameView(LoginRequiredMixin, ListView):
    """"""
    
    login_url = "/id"
    model = Game
    template_name = "bracket/game_page.html"

    def get(self, request, game_id):
        if len(game := Game.objects.filter(id=game_id)) > 0:
            game = game[0]
            
            ctx = {
                "id": game.id,
                "fase": number_to_fase[game.wc_round],
                "team_1": game.team_1,
                "flag_1": game.team_1.flag_fifa_url,
                "abbr_1": game.team_1.abbr,
                "score_team_1":game.score_team_1,
                "team_2": game.team_2,
                "flag_2": game.team_2.flag_fifa_url,
                "abbr_2": game.team_2.abbr,
                "score_team_2":game.score_team_2
            }
            if game.game_date == datetime.now(pytz.timezone('America/Bogota')).date() and (game.score_team_1 == None or game.score_team_2 == None):
                
                ctx["score_team_1"] = "TBD"
                ctx["score_team_2"] = "TBD"

            return render(request, self.template_name, ctx)
        return redirect("home:my_predictions")


class FinishedGamesListView(LoginRequiredMixin,View):
    """"""
    login_url = "/id"
    template_name: str = "bracket/completed_games.html"

    def get(self, request):
        games : List[Game] = Game.objects.filter(~Q(score_team_1=None) & ~Q(score_team_2=None)).order_by("game_date","game_time")
        ctx = {"data":{}}
        for g in games:
            preds = g.game_predictions.all()
            marcador = preds.filter(correct=2)
            ganador = preds.filter(correct__gt=0)
            t1,t2 = list(zip(*[p.predicted_score.split("-") for p in preds]))
            avg_score_team = lambda t : str(round(sum(map(int,t))/len(t),2))
            avg_score = " - ".join([avg_score_team(t1),avg_score_team(t2)])
            game_data = {
                "id":g.id,
                "team_1":g.team_1,
                "team_2":g.team_2,
                "score_team_1":g.score_team_1,
                "score_team_2":g.score_team_2,
                "p_winner":round(len(ganador)/len(preds),2),
                "p_score":round(len(marcador)/len(preds),2),
                "avg_points": round((2*len(marcador)+2*len(ganador))/len(preds),2),
                "avg_pred": avg_score
            }
            # print(game_data)
            if len(ctx["data"]) == 0 or g.game_date not in ctx["data"].keys():
               ctx["data"][g.game_date] = [game_data]
            else:
                ctx["data"][g.game_date].append(game_data)
            
        return render(request, self.template_name, ctx)

class PredListView(LoginRequiredMixin,ListView):
    """"""
    login_url = "/id"
    model = Prediction
    template_name: str = "bracket/prediction_list.html"

    def get(self, request, username=None):
        ctx = {"username": username if username else request.user}
        return render(request, self.template_name, ctx)


class BracketView(LoginRequiredMixin, View):
    context_object_name = "ctx"
    login_url = "/id"
    def get(self, request, username=None):
        if len(pred := BracketPrediction.objects.filter(owner=username if username else request.user)) > 0:
            full_bracket = pred[0].get_bracket()

            ctx = {"completed": True, "bracket": full_bracket}

        else:
            countries = Country.objects.all().order_by("group")
            ctx = {
                "completed": False,
                "A": countries[0:4],
                "B": countries[4:8],
                "C": countries[8:12],
                "D": countries[12:16],
                "E": countries[16:20],
                "F": countries[20:24],
                "G": countries[24:28],
                "H": countries[28:32],
            }
        return render(request, "bracket/grand_bracket_page.html", context=ctx)
