from django.urls import path
from . import views

app_name='bracket'
urlpatterns = [
    path('open', views.OpenView.as_view(), name='open'),
    path('apereo', views.ApereoView.as_view(), name='apereo'),
    path('manual', views.ManualProtect.as_view(), name='manual'),
    path('protect', views.ProtectView.as_view(), name='protect'),
    path('python', views.DumpPython.as_view(), name='python'),
]