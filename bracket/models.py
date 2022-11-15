from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here
class Country(models.Model):
    """
    Represents a team competing in the WC
    """

    name = models.CharField(max_length=20)
    abbr = models.CharField(max_length=3)
    group = models.CharField(max_length=1)

    finish_rank = models.CharField(max_length=8, blank=True, null=True)
    game_won = models.IntegerField(default=0)
    goals_plus = models.IntegerField(default=0)
    goals_minus = models.IntegerField(default=0)

    def set_result(
        self,
    ):
        # TODO: update model with match result
        pass

    def __str__(self) -> str:
        return f"{self.name} {self.finish_rank if self.finish_rank else ''}"


class Game(models.Model):
    """
    Represents a game played
    """

    GR = 0
    SECOND = 1
    THIRD = 2
    SEMI = 3
    FINAL = 4

    ROUNDS = [
        (GR, "Grupos"),
        (SECOND, "16"),
        (THIRD, "Cuartos de Final"),
        (SEMI, "Semi-Final"),
        (FINAL, "Final"),
    ]

    wc_round = models.IntegerField(default=0, choices=ROUNDS)

    game_date = models.DateField(auto_now=False, auto_now_add=False)
    game_time = models.TimeField(auto_now=False, auto_now_add=False)

    team_1 = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.CASCADE, related_name="team_1"
    )
    score_team_1 = models.IntegerField(blank=True, null=True)

    team_2 = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.CASCADE, related_name="team_2"
    )
    score_team_2 = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.team_1} - {self.team_2} {"fase de " if self.wc_round<=2 else "" }{self.ROUNDS[self.wc_round][1]}'


class UsersPoints(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="points")
    points = models.IntegerField(default=0)
    # all_predictions_done = models.BooleanField(default=False)

    def _add_points(self, points):
        self.points += points
        self.save(update_fields=["points"])

    def __str__(self) -> str:
        return f"{self.owner.username} -> {self.points}"


class Prediction(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="predictions"
    )
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name="game_predictions"
    )

    team_1 = "TEAM_1"
    team_2 = "TEAM_2"
    teams = [(team_1, "TEAM_1"), (team_1, "TEAM_2")]

    # predicted_winner = models.CharField(max_length=6, choices=teams)
    predicted_score = models.CharField(max_length=5)

    correct = models.IntegerField(blank=True, null=True)

    def _mark_correct(self, st1, st2):
        pst1, pst2 = self.predicted_score.split("-")

        c = calc_c(st1,st2,pst1,pst2)

        
        self.correct = c
        self.save(update_fields=["correct"])

    @staticmethod
    def format_prediction_dict(request, game_id):
        pred_winner = None
        if request.data.get("score_team_1") > request.data.get("score_team_2"):
            pred_winner = Prediction.team_1
        elif request.data.get("score_team_2") > request.data.get("score_team_1"):
            pred_winner = Prediction.team_2

        new_prediction = {
            "owner": request.user.id,
            "game": game_id,
            "predicted_winner": pred_winner,
            "predicted_score": "-".join(
                [request.data.get("score_team_1"), request.data.get("score_team_2")]
            ),
        }
        return new_prediction

    def __str__(self) -> str:
        return f"{self.predicted_score} {self.game}"


def update_predition_correct(sender, instance: Game, **kwargs):
    # print("triggered update_predition_correct")
    # print("------------------------------")
    if instance.score_team_1 is not None and instance.score_team_2 is not None:
        predictions = Prediction.objects.filter(game=instance)
        for pred in predictions:
            pred._mark_correct(instance.score_team_1, instance.score_team_2)


def update_points(sender, instance: Prediction, **kwargs):
    """
    1: Acertar quien gana el partido sin el marcador 2 puntos.
    2: Acertar el marcador 4 puntos por partido.
    3: Acertar el orden de clasificación en cada grupo 3 puntos por cada grupo al finalizar la ronda de grupos.
    Duplicar esos puntos para cada la siguiente fase (16 avos) y hacer lo mismo para las semifinales y finales."""
    # print("triggered update_points")
    if not instance.correct in (0,1,2):
        return
    owner = instance.owner
    points = {
        0: 0,
        1: 2,
        2: 4,
    }
    multiplier = {
        Game.GR: 1,
        Game.SECOND: 2,
        Game.THIRD: 4,
        Game.SEMI: 8,
        Game.FINAL: 16,
    }

    p = points[instance.correct] * multiplier[instance.game.wc_round]
    owner.points._add_points(p)

def calc_c(r1,r2,p1,p2) -> int:
    [r1,r2,p1,p2] = list(map(int,[r1,r2,p1,p2]))
    # print(r1,r2,p1,p2,(r1 == p1),(r2 == p2))
    if (r1 == p1) and (r2 == p2): #predicted everything
        # print("predicted everything")
        return 2
    if (r1 == r2) and p1 == p2: #predicted tie
        # print("predicted tie")
        return 1
    if (r1 > r2) and (p1 > p2): #predicted t1 wins
        # print("predicted t1 wins")
        return 1
    if (r1 < r2) and (p1 < p2): #predicted t2 wins
        # print("predicted t2 wins")
        return 1
    # print("predicted wrong")
    return 0 #predicted wrong

post_save.connect(update_predition_correct, sender=Game)
post_save.connect(update_points, sender=Prediction)
