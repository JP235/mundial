from datetime import datetime
from typing import List
import pytz
from itertools import accumulate

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from .models import (
    Game,
    Prediction,
    Country,
    BracketPrediction,
    UsersPoints,
    User,
    WinnerPrediction,
)

number_to_fase = {
    1: "Octavos de Final",
    2: "Cuartos de Final",
    3: "Semi-Final",
    4: "Final",
}


class LoggedInView(LoginRequiredMixin, View):
    """"""

    login_url = "/id"


class GameView(LoggedInView):
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
                "flag_1": game.team_1.flag_fifa_url,
                "abbr_1": game.team_1.abbr,
                "score_team_1": game.score_team_1,
                "team_2": game.team_2,
                "flag_2": game.team_2.flag_fifa_url,
                "abbr_2": game.team_2.abbr,
                "score_team_2": game.score_team_2,
            }
            if game.game_date == datetime.now(
                pytz.timezone("America/Bogota")
            ).date() and (game.score_team_1 == None or game.score_team_2 == None):

                ctx["score_team_1"] = "TBD"
                ctx["score_team_2"] = "TBD"

            return render(request, self.template_name, ctx)
        return redirect("home:my_predictions")


class FinishedGamesListView(LoggedInView):
    """"""

    login_url = "/id"
    template_name: str = "bracket/completed_games.html"

    def get(self, request):
        games: List[Game] = Game.objects.all().order_by("game_date", "game_time")
        ctx = {"data": {}}
        for g in games:
            preds = g.game_predictions.all()
            marcador = preds.filter(correct=2)
            ganador = preds.filter(correct__gt=0)
            finished_game = g.score_team_1 is not None

            if len(preds) == 0:
                game_data = {
                    "id": g.id,
                    "team_1": g.team_1,
                    "team_2": g.team_2,
                    "round": number_to_fase[g.wc_round],
                    "group": g.team_1.group,
                    "score_team_1": g.score_team_1 if finished_game else "",
                    "score_team_2": g.score_team_2 if finished_game else "",
                    "p_winner": "-",
                    "p_score": "-",
                    "avg_points": "-",
                    "avg_pred": "-",
                }
            else:
                t1, t2 = list(
                    zip(*[p.predicted_score.split("-") for p in preds])
                )  # ('1-2') ('0-0') ('6-3')-> ('1','0','6'),('2','0','3')
                fstr_2_dec = lambda n: f"{n:.2f}"
                str_avg_score_team = lambda t: fstr_2_dec(sum(map(int, t)) / len(t))
                avg_pred = " - ".join([str_avg_score_team(t1), str_avg_score_team(t2)])
                game_data = {
                    "id": g.id,
                    "team_1": g.team_1,
                    "team_2": g.team_2,
                    "round": number_to_fase[g.wc_round],
                    "group": g.team_1.group,
                    "score_team_1": g.score_team_1 if finished_game else "",
                    "score_team_2": g.score_team_2 if finished_game else "",
                    "p_winner": fstr_2_dec(len(ganador) / len(preds))
                    if finished_game
                    else "-",
                    "p_score": fstr_2_dec(len(marcador) / len(preds))
                    if finished_game
                    else "-",
                    "avg_points": fstr_2_dec(
                        (2 * len(marcador) + 2 * len(ganador)) / len(preds)
                    )
                    if finished_game
                    else "-",
                    "avg_pred": avg_pred,
                }
            if len(ctx["data"]) == 0 or g.game_date not in ctx["data"].keys():
                ctx["data"][g.game_date] = [game_data]
            else:
                ctx["data"][g.game_date].append(game_data)

        return render(request, self.template_name, ctx)


class PredListView(LoggedInView):
    """"""

    login_url = "/id"
    template_name: str = "bracket/prediction_list.html"

    def get(self, request, username=None):
        req_user = username if username else request.user

        if not UsersPoints.avg_per_game():
            ctx = {
                "username": req_user,
            }
            return render(request, self.template_name, ctx)

        day_labels, avg_day = list(zip(*UsersPoints.avg_per_day().items()))
        game_labels, avg_game = list(zip(*UsersPoints.avg_per_game().items()))

        game_labels = [
            # n
            " - ".join(g.split(" - ")[0:2])
            for n, g in enumerate(game_labels)
        ]  # remove round

        user = User.objects.get(username=req_user)
        _, user_day = list(zip(*user.points.points_per_day.items()))
        _, user_game = list(zip(*user.points.points_per_game.items()))

        user_total_day = accumulate(user_day)
        user_total_game = accumulate(user_game)

        avg_total_day = accumulate(avg_day)
        avg_total_game = accumulate(avg_game)

        fstr_2_dec = lambda n: f"{n:.2f}"

        avg_day = list(map(fstr_2_dec, avg_day))
        avg_total_day = list(map(fstr_2_dec, avg_total_day))

        avg_game = list(map(fstr_2_dec, avg_game))
        avg_total_game = list(map(fstr_2_dec, avg_total_game))

        ctx = {
            "username": req_user,
            "day_labels": day_labels,
            "user_day": user_day,
            "user_total_day": user_total_day,
            "avg_day": avg_day,
            "avg_total_day": avg_total_day,
            "game_labels": game_labels,
            "user_game": user_game,
            "avg_game": avg_game,
            "user_total_game": user_total_game,
            "avg_total_game": avg_total_game,
        }
        return render(request, self.template_name, ctx)


class WinnerPredView(LoggedInView):
    """ """

    def get(self, request, username=None):
        req_user = username if username else request.user

        countries = Country.objects.all().order_by("group")

        ctx = {"countries": countries}
        if len(pred := WinnerPrediction.objects.filter(owner=req_user)) > 0:
            user_winner = pred[0].winner
            ctx["completed"] = True
            ctx["winner"] = user_winner

        else:
            ctx["completed"] = False
        return render(request, "bracket/winner_prediction_page.html", context=ctx)


class BracketView(LoggedInView):
    context_object_name = "ctx"
    login_url = "/id"

    def get(self, request, username=None):
        if (
            len(
                pred := BracketPrediction.objects.filter(
                    owner=username if username else request.user
                )
            )
            > 0
        ):
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
