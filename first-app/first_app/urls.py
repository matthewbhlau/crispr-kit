from django.urls import path

from .views import main, results

urlpatterns = [
    path("main/", main, name="main-page"),
    path("result/", results, name="results")
]
