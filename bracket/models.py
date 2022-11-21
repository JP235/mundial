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
    flag_fifa_url = models.URLField(max_length=200, blank=True, null=True)

    def set_result(
        self,
    ):
        # TODO: update model with match result
        pass

    def __str__(self) -> str:
        return f"{self.name} {self.finish_rank if self.finish_rank else ''}"


class GroupError(Exception):
    def __init__(self, group: str, T1: Country, T2: Country):
        self.message = \
                f"Grupo {group} recivió equipos: Primero: {T1.name} Segundo: {T2.name}"
        super().__init__(self.message)


def check_group(group: str, T1: Country, T2: Country):
    if T1 == T2:
        raise GroupError(group, T1, T2)
    if not ((T1.group == group) and (T2.group == group)):
        raise GroupError(group, T1, T2)
    return T1, T2


def validate_winners_input(*args):
    for w in args:
        if w not in (1, 2):
            raise ValueError(f"Hay que seleccionar ganador para todos los partidos. {args}")
    return args


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
        return f'{self.team_1} - {self.team_2}'


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

        c = calc_c(st1, st2, pst1, pst2)

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
                [str(int(request.data.get("score_team_1"))), str(int(request.data.get("score_team_2")))]
            ),
        }
        return new_prediction

    def __str__(self) -> str:
        return f"{self.predicted_score} {self.game}"


def update_predition_correct(instance: Game, **kwargs):
    # print("triggered update_predition_correct")
    # print("------------------------------")
    if instance.score_team_1 is not None and instance.score_team_2 is not None:
        predictions = Prediction.objects.filter(game=instance)
        for pred in predictions:
            pred._mark_correct(instance.score_team_1, instance.score_team_2)


def update_points(instance: Prediction, **kwargs):
    """
    1: Acertar quien gana el partido sin el marcador 2 puntos.
    2: Acertar el marcador 4 puntos por partido.
    3: Acertar el orden de clasificación en cada grupo 3 puntos por cada grupo al finalizar la ronda de grupos."""
    # print("triggered update_points")
    if not instance.correct in (0, 1, 2):
        return
    owner = instance.owner
    points = {
        0: 0,
        1: 2,
        2: 4,
    }
    multiplier = {
        Game.GR: 1,
        Game.SECOND: 1,
        Game.THIRD: 1,
        Game.SEMI: 1,
        Game.FINAL: 1,
    }

    p = points[instance.correct] * multiplier[instance.game.wc_round]
    owner.points._add_points(p)


def calc_c(r1, r2, p1, p2) -> int:
    [r1, r2, p1, p2] = list(map(int, [r1, r2, p1, p2]))
    # print(r1,r2,p1,p2,(r1 == p1),(r2 == p2))
    if (r1 == p1) and (r2 == p2):  # predicted everything
        # print("predicted everything")
        return 2
    if (r1 == r2) and p1 == p2:  # predicted tie
        # print("predicted tie")
        return 1
    if (r1 > r2) and (p1 > p2):  # predicted t1 wins
        # print("predicted t1 wins")
        return 1
    if (r1 < r2) and (p1 < p2):  # predicted t2 wins
        # print("predicted t2 wins")
        return 1
    # print("predicted wrong")
    return 0  # predicted wrong


post_save.connect(update_predition_correct, sender=Game)
post_save.connect(update_points, sender=Prediction)


class BracketPrediction(models.Model):
    """
    Represents a full bracket prediction
    """

    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="bracket_prediction"
    )

    A1 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="A1")
    A2 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="A2")
    B1 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="B1")
    B2 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="B2")
    C1 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="C1")
    C2 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="C2")
    D1 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="D1")
    D2 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="D2")
    E1 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="E1")
    E2 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="E2")
    F1 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="F1")
    F2 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="F2")
    G1 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="G1")
    G2 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="G2")
    H1 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="H1")
    H2 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="H2")
    A1B2 = models.IntegerField(default=0)
    C1D2 = models.IntegerField(default=0)
    E1F2 = models.IntegerField(default=0)
    G1H2 = models.IntegerField(default=0)
    B1A2 = models.IntegerField(default=0)
    D1C2 = models.IntegerField(default=0)
    F1E2 = models.IntegerField(default=0)
    H1G2 = models.IntegerField(default=0)

    AD = models.IntegerField(default=0)
    EH = models.IntegerField(default=0)
    BC = models.IntegerField(default=0)
    FG = models.IntegerField(default=0)

    AH = models.IntegerField(default=0)
    BG = models.IntegerField(default=0)

    winner = models.IntegerField(default=0)

    @staticmethod
    def format_request(request):
        new_prediction = {
            "owner": request.user.id,
            "A1": Country.objects.get(abbr=request.data.get("A1")).pk,
            "A2": Country.objects.get(abbr=request.data.get("A2")).pk,
            "B1": Country.objects.get(abbr=request.data.get("B1")).pk,
            "B2": Country.objects.get(abbr=request.data.get("B2")).pk,
            "C1": Country.objects.get(abbr=request.data.get("C1")).pk,
            "C2": Country.objects.get(abbr=request.data.get("C2")).pk,
            "D1": Country.objects.get(abbr=request.data.get("D1")).pk,
            "D2": Country.objects.get(abbr=request.data.get("D2")).pk,
            "E1": Country.objects.get(abbr=request.data.get("E1")).pk,
            "E2": Country.objects.get(abbr=request.data.get("E2")).pk,
            "F1": Country.objects.get(abbr=request.data.get("F1")).pk,
            "F2": Country.objects.get(abbr=request.data.get("F2")).pk,
            "G1": Country.objects.get(abbr=request.data.get("G1")).pk,
            "G2": Country.objects.get(abbr=request.data.get("G2")).pk,
            "H1": Country.objects.get(abbr=request.data.get("H1")).pk,
            "H2": Country.objects.get(abbr=request.data.get("H2")).pk,
            "A1B2": request.data.get("A1B2"),
            "C1D2": request.data.get("C1D2"),
            "E1F2": request.data.get("E1F2"),
            "G1H2": request.data.get("G1H2"),
            "B1A2": request.data.get("B1A2"),
            "D1C2": request.data.get("D1C2"),
            "F1E2": request.data.get("F1E2"),
            "H1G2": request.data.get("H1G2"),
            "AD": request.data.get("AD"),
            "EH": request.data.get("EH"),
            "BC": request.data.get("BC"),
            "FG": request.data.get("FG"),
            "AH": request.data.get("AH"),
            "BG": request.data.get("BG"),
            "winner": request.data.get("winner"),
        }
        return new_prediction

    def save(self, *args, **kwargs):

        self._validate_groups()
        self._validate_sixteen()
        self._validate_eight()
        self._validate_semi()
        self._validate_final()
        super().save(*args, **kwargs)

    def get_bracket(self):
        sixteen = {
            "A1": self.A1,
            "A2": self.A2,
            "B1": self.B1,
            "B2": self.B2,
            "C1": self.C1,
            "C2": self.C2,
            "D1": self.D1,
            "D2": self.D2,
            "E1": self.E1,
            "E2": self.E2,
            "F1": self.F1,
            "F2": self.F2,
            "G1": self.G1,
            "G2": self.G2,
            "H1": self.H1,
            "H2": self.H2,
        }

        eight = {
            "A1B2": [sixteen["A1"], sixteen["B2"]][self.A1B2 - 1],
            "C1D2": [sixteen["C1"], sixteen["D2"]][self.C1D2 - 1],
            "E1F2": [sixteen["E1"], sixteen["F2"]][self.E1F2 - 1],
            "G1H2": [sixteen["G1"], sixteen["H2"]][self.G1H2 - 1],
            "B1A2": [sixteen["B1"], sixteen["A2"]][self.B1A2 - 1],
            "D1C2": [sixteen["D1"], sixteen["C2"]][self.D1C2 - 1],
            "F1E2": [sixteen["F1"], sixteen["E2"]][self.F1E2 - 1],
            "H1G2": [sixteen["H1"], sixteen["G2"]][self.H1G2 - 1],
        }
        semi = {
            "AD": [eight["A1B2"], eight["C1D2"]][self.AD - 1],
            "EH": [eight["E1F2"], eight["G1H2"]][self.EH - 1],
            "BC": [eight["B1A2"], eight["D1C2"]][self.BC - 1],
            "FG": [eight["F1E2"], eight["H1G2"]][self.FG - 1],
        }
        final = {
            "AH": [semi["AD"], semi["EH"]][self.AH - 1],
            "BG": [semi["BC"], semi["FG"]][self.BG - 1],
        }
        winner = {"winner": [final["AH"], final["BG"]][self.winner - 1]}
        return {
            "sixteen": sixteen,
            "eight": eight,
            "semi": semi,
            "final": final,
            "winner": winner,
        }

    def _validate_groups(self):
        self.A1, self.A2 = check_group("A", self.A1, self.A2)
        self.B1, self.B2 = check_group("B", self.B1, self.B2)
        self.C1, self.C2 = check_group("C", self.C1, self.C2)
        self.D1, self.D2 = check_group("D", self.D1, self.D2)
        self.E1, self.E2 = check_group("E", self.E1, self.E2)
        self.F1, self.F2 = check_group("F", self.F1, self.F2)
        self.G1, self.G2 = check_group("G", self.G1, self.G2)
        self.H1, self.H2 = check_group("H", self.H1, self.H2)

    def _validate_sixteen(self):
        (
            self.A1B2,
            self.C1D2,
            self.E1F2,
            self.G1H2,
            self.B1A2,
            self.D1C2,
            self.F1E2,
            self.H1G2,
        ) = validate_winners_input(
            self.A1B2,
            self.C1D2,
            self.E1F2,
            self.G1H2,
            self.B1A2,
            self.D1C2,
            self.F1E2,
            self.H1G2,
        )

    def _validate_eight(self):
        self.AD, self.EH, self.BC, self.FG = validate_winners_input(
            self.AD, self.EH, self.BC, self.FG
        )

    def _validate_semi(self):
        self.AH, self.BG = validate_winners_input(self.AH, self.BG)

    def _validate_final(self):
        self.winner = validate_winners_input(self.winner)[0]

    def __str__(self) -> str:
        return f'{self.owner}, {self.get_bracket()["winner"]["winner"]}'