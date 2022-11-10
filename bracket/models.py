from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Country(models.Model):
    """
    Represents a team competing in the WC
    """

    name = models.CharField(max_length=20)
    abbr = models.CharField(max_length=3) 
    group = models.CharField(max_length=1)

    finish_rank = models.IntegerField(blank=True,null=True)
    game_won = models.IntegerField(default = 0)
    goals_plus = models.IntegerField(default = 0)
    goals_minus = models.IntegerField(default = 0)

    def set_result(self, ):
        #TODO: update model with match result
        pass

    def __str__(self) -> str:
        
        return f"{self.name}  #{self.finish_rank if self.finish_rank else 'TBD'}" 

class Match(models.Model):
    """
    Represents a match played
    """
    GR = 1
    SECOND = 2
    THIRD = 3
    SEMI = 4
    FINAL = 5

    ROUNDS = [
        (GR, 'Grupos'),
        (SECOND, '16'),
        (THIRD, 'Cuartos de Final'),
        (SEMI, 'Semi-Final'),
        (FINAL, 'Final')
        ]

    wc_round = models.IntegerField(default=0,choices=ROUNDS)

    winner = models.ForeignKey(
        Country,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="Winner"
        )
    scoreW = models.IntegerField(null=True)
    
    looser = models.ForeignKey(
        Country,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="Looser"
        )
    scoreL = models.IntegerField(null=True)