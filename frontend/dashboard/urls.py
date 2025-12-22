from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("admin-panel/", views.admin_panel, name="admin_panel"),
    path("panel/add-candidate/", views.add_candidate, name="add_candidate"),
    path("panel/start-election/", views.start_election, name="start_election"),
    path("panel/end-election/", views.end_election, name="end_election"),
    path("panel/reset-election/", views.reset_election, name="reset_election"),
    path("vote/", views.vote_view, name="vote"),
    path("results/", views.results_view, name="results"),
]
