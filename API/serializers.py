from django.contrib.auth.models import User
from rest_framework import serializers
from bracket.views import number_to_fase
from bracket.models import Game, Prediction, Country, BracketPrediction, WinnerPrediction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["points"] = User.objects.filter(id=data["id"])[0].points.points
        try:
            data["winner_abbr"] = WinnerPrediction.objects.filter(owner=data["id"])[0].winner.abbr
            data["winner_flag"] = WinnerPrediction.objects.filter(owner=data["id"])[0].winner.flag_fifa_url
        except IndexError:
            data["winner_abbr"] = "FIFA" 
            data["winner_flag"] = "https://upload.wikimedia.org/wikipedia/commons/1/1f/FIFA_Flag.svg"
        return data


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["team_1"] = Country.objects.filter(id=data["team_1"])[0].name
        data["team_2"] = Country.objects.filter(id=data["team_2"])[0].name
        if data["score_team_1"]:
            data["score"] = "-".join(
                list(map(str, [data["score_team_1"], data["score_team_2"]]))
            )
        else:
            data["score"] = "TBD"
        return data

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return data

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["name","abbr","group","flag_fifa_url"]

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = "__all__"

    def to_representation(self, instance):
        """
        fields out -> {
            correct
            null
            game
            id
            owner
            predicted_score
            round
            team_1
            team_2
        }
        """
        data_out = super().to_representation(instance)

        data_out["owner"] = User.objects.get(id=data_out["owner"]).username
        data_out["round"] = number_to_fase[
            int(Game.objects.get(pk=data_out.get("game")).wc_round.__str__())
        ]
        g = Game.objects.get(pk=data_out.get("game"))
        data_out["team_1"] = g.team_1.name
        data_out["team_2"] = g.team_2.name
        data_out["score"] = "-".join([str(g.score_team_1),str(g.score_team_2)]) if g.score_team_2 != None else "-"
        return data_out

class BracketPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BracketPrediction
        fields = "__all__"
    def to_internal_value(self, instance):
        data = super().to_internal_value(instance)
        # print(data)
        return data
