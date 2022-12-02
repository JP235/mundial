from django.contrib import admin

from .models import Country,Game,Prediction,UsersPoints,BracketPrediction,WinnerPrediction
# Register your models here.

admin.site.register(Country)
admin.site.register(Game)
admin.site.register(Prediction)
admin.site.register(UsersPoints)
admin.site.register(BracketPrediction)
admin.site.register(WinnerPrediction)