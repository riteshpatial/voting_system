from django.shortcuts import render, redirect
from django.contrib import messages
import requests

API_BASE = "http://127.0.0.1:5000/api"

def home_view(request):
    try:
        state = requests.get(f"{API_BASE}/state").json()["state"]
    except Exception:
        state = 0

    status_msg = {
        0: "Election not started",
        1: "Voting is live",
        2: "Election ended"
    }[state]

    return render(request, "dashboard/home.html", {
        "state": state,
        "status_msg": status_msg
    })

def admin_panel(request):
    from .models import Voter
    voters = Voter.objects.all()
    return render(request, "dashboard/admin_panel.html", {"voters": voters})

def add_candidate(request):
    requests.post(f"{API_BASE}/add-candidate", json={"name": request.POST["name"]})
    return redirect("admin_panel")

def start_election(request):
    requests.post(f"{API_BASE}/start-election")
    messages.success(request, "Election started")
    return redirect("admin_panel")

def end_election(request):
    requests.post(f"{API_BASE}/end-election")
    messages.success(request, "Election ended")
    return redirect("admin_panel")

def reset_election(request):
    from .models import Voter
    Voter.objects.all().delete()
    requests.post(f"{API_BASE}/reset-election")
    messages.success(request, "New election initialized")
    return redirect("admin_panel")

def vote_view(request):
    candidates = requests.get(f"{API_BASE}/candidates").json()

    if request.method == "POST":
        r = requests.post(f"{API_BASE}/vote", json={
            "candidate_id": int(request.POST["candidate_id"]),
            "private_key": request.POST["private_key"]
        })
        messages.info(request, r.json()["message"])
        return redirect("vote")

    return render(request, "dashboard/vote.html", {"candidates": candidates})

def results_view(request):
    state = requests.get(f"{API_BASE}/state").json()["state"]
    if state != 2:
        messages.error(request, "Results not available yet")
        return redirect("home")

    results = requests.get(f"{API_BASE}/candidates").json()
    return render(request, "dashboard/results.html", {"results": results})
