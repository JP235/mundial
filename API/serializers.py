from django.contrib.auth.models import User
from rest_framework import serializers

from bracket.models import Game, UsersPoints, Prediction, Country

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username" ]
    
    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data["points"] = User.objects.filter(id = data["id"])[0].points.points
        return data

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        exclude = ["id"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        data["team_1"] = Country.objects.filter(id = data["team_1"])[0].name
        data["team_2"] = Country.objects.filter(id = data["team_2"])[0].name
        if data["score_team_1"]:
            data["score"] =  "-".join(list(map(str,[data["score_team_1"],data["score_team_2"]])))
        else:
             data["score"] =  "TBD"

        return data
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return data

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = "__all__"
    def to_representation(self, instance):
        # print(instance)
        return super().to_representation(instance)