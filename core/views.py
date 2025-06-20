from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Position, Candidate, Vote

def welcome(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/welcome.html')

def user_register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'core/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'core/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('welcome')

@login_required
def dashboard(request):
    positions = Position.objects.all()
    voted_positions = Vote.objects.filter(user=request.user).values_list('position_id', flat=True)
    return render(request, 'core/dashboard.html', {
        'positions': positions,
        'voted_positions': voted_positions
    })

@login_required
def vote_position(request, position_id):
    position = get_object_or_404(Position, id=position_id)
    candidates = Candidate.objects.filter(position=position)
    if request.method == 'POST':
        if not Vote.objects.filter(user=request.user, position=position).exists():
            selected_id = request.POST.get('candidate')
            selected_candidate = get_object_or_404(Candidate, id=selected_id)
            Vote.objects.create(user=request.user, candidate=selected_candidate, position=position)
        return redirect('dashboard')
    return render(request, 'core/vote.html', {
        'position': position,
        'candidates': candidates
    })

@login_required
def result(request):
    positions = Position.objects.all()
    result_data = []
    for pos in positions:
        candidates = Candidate.objects.filter(position=pos)
        total_votes = Vote.objects.filter(position=pos).count()
        stats = []
        for c in candidates:
            vote_count = Vote.objects.filter(candidate=c).count()
            stats.append({
                'candidate': c,
                'votes': vote_count,
                'percentage': (vote_count / total_votes) * 100 if total_votes > 0 else 0
            })
        stats.sort(key=lambda x: x['votes'], reverse=True)
        result_data.append({'position': pos, 'stats': stats})
    return render(request, 'core/result.html', {'results': result_data})