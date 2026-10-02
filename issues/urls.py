from django.urls import path
from . import views


urlpatterns = [
    path("reporters/", views.route_reporters_root),
    path("issues/", views.route_issues_root),
]
