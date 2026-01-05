from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import subprocess
import sys
import os

API_BASE = "http://127.0.0.1:5000/api"


# ======================
# HOME
# ======================
def home_view(request):
    """
    Home page.
    Message about results should appear ONLY
    when user clicks 'View Results'.
    """
    return render(request, "dashboard/home.html")


# ======================
# ADMIN PANEL
# ======================
def admin_panel(request):
    from .models import Voter

    voters = Voter.objects.all().order_by("-id")

    return render(
        request,
        "dashboard/admin_panel.html",
        {"voters": voters},
    )


# ======================
# ADMIN ACTIONS
# ======================
def add_candidate(request):
    if request.method == "POST":
        name = request.POST.get("name")

        if not name:
            messages.error(request, "Candidate name required")
            return redirect("admin_panel")

        try:
            r = requests.post(f"{API_BASE}/add-candidate", json={"name": name})
        except Exception:
            messages.error(request, "Blockchain service not reachable")
            return redirect("admin_panel")

        if r.status_code == 200:
            messages.success(request, "Candidate added successfully")
        else:
            messages.error(request, "Blockchain error while adding candidate")

    return redirect("admin_panel")


def start_election(request):
    r = requests.post(f"{API_BASE}/start-election")

    if r.status_code == 200:
        # 🔓 Unlock results
        request.session.pop("force_results_lock", None)
        messages.success(request, "Election started")
    else:
        messages.error(request, "Election already started or blockchain error")

    return redirect("admin_panel")



def end_election(request):
    try:
        r = requests.post(f"{API_BASE}/end-election")
    except Exception:
        messages.error(request, "Blockchain service not reachable")
        return redirect("admin_panel")

    if r.status_code == 200:
        messages.success(request, "Election ended")
    else:
        messages.error(request, "Election not active or blockchain error")

    return redirect("admin_panel")


# ======================
# 🔁 FULL RESET ELECTION
# ======================
def reset_election(request):
    """
    Reset election for new cycle.
    Blockchain stays same, UI logic resets.
    """
    from .models import Voter

    # Clear local voters
    Voter.objects.all().delete()

    # 🔐 LOCK RESULTS explicitly
    request.session["force_results_lock"] = True

    messages.success(
        request,
        "New election initialized successfully. Results locked."
    )

    return redirect("admin_panel")


# ======================
# REGISTER VOTER
# ======================
def register_voter(request):
    from .models import Voter

    if request.method == "POST":
        voter_address = request.POST.get("voter_address")
        private_key = request.POST.get("private_key")

        if not voter_address or not private_key:
            messages.error(request, "All fields required")
            return redirect("register_voter")

        voter, created = Voter.objects.get_or_create(
            voter_address=voter_address,
            defaults={"private_key": private_key},
        )

        if created:
            messages.success(request, "Voter registered")
        else:
            messages.info(request, "Voter already exists")

        return redirect("admin_panel")

    return render(request, "dashboard/register_voter.html")


# ======================
# CAST VOTE
# ======================
def vote_view(request):
    from .models import Voter

    # 1️⃣ Check election state
    try:
        state = requests.get(f"{API_BASE}/state").json()["state"]
    except Exception:
        state = 0

    # ❌ Election not active → hide candidates
    if state != 1:
        return render(
            request,
            "dashboard/vote.html",
            {
                "candidates": [],
                "inactive": True
            }
        )

    # 2️⃣ Election active → fetch candidates
    try:
        candidates = requests.get(f"{API_BASE}/candidates").json()
    except Exception:
        candidates = []

    if request.method == "POST":
        candidate_id = request.POST.get("candidate_id")
        private_key = request.POST.get("private_key")

        if not candidate_id or not private_key:
            messages.error(request, "All fields are required")
            return redirect("vote")

        if not Voter.objects.filter(private_key=private_key).exists():
            messages.error(request, "You are not a registered voter")
            return redirect("vote")

        vr = requests.post(
            f"{API_BASE}/vote",
            json={
                "candidate_id": int(candidate_id),
                "private_key": private_key,
            },
        )

        if vr.status_code == 200:
            messages.success(request, "Vote cast successfully")
        else:
            messages.error(request, "Voting failed or already voted")

        return redirect("vote")

    return render(
        request,
        "dashboard/vote.html",
        {
            "candidates": candidates,
            "inactive": False
        }
    )



# ======================
# RESULTS
# ======================
def results_view(request):
    """
    Results visible ONLY when:
    - Election ended
    - AND not manually locked after reset
    """

    # 🔒 HARD LOCK AFTER RESET
    if request.session.get("force_results_lock"):
        return render(
            request,
            "dashboard/home.html",
            {
                "result_error_msg": "Results are locked. New election has not ended yet."
            },
        )

    try:
        state = requests.get(f"{API_BASE}/state").json().get("state", 0)
    except Exception:
        state = 0

    # Election not ended
    if state != 2:
        return render(
            request,
            "dashboard/home.html",
            {
                "result_error_msg": "Results are available only after election ends."
            },
        )

    # Election ended → show results
    try:
        results = requests.get(f"{API_BASE}/candidates").json()
    except Exception:
        results = []

    return render(
        request,
        "dashboard/results.html",
        {"results": results}
    )
