from django.urls import path, include
from django.views.generic import TemplateView

app_name='id'
urlpatterns = [
    path('', TemplateView.as_view(template_name='identification/login_register.html'),name="id"),
    path('reg', TemplateView.as_view(template_name='identification/register.html'),name="idreg"),
]