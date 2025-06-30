from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Position, Candidate, Vote
from .forms import StudentRegisterForm, StudentLoginForm

def welcome(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/welcome.html')

def user_register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = StudentRegisterForm(request.POST or None)
    if form.is_valid():
        student_id = form.cleaned_data['student_id']
        if User.objects.filter(username=student_id).exists():
            messages.success(request, 'An account with this Student ID already exists.')
            return render(request, 'core/account_exists.html')
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        nickname = form.cleaned_data['nickname']

        user = User.objects.create_user(username=student_id)
        user.set_password(password)
        user.save()

        user.profile.student_id = student_id
        user.profile.email = email
        user.profile.nickname = nickname
        user.profile.save()

        login(request, user)
        return redirect('dashboard')
    return render(request, 'core/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = StudentLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        student_id = form.cleaned_data['student_id']
        password = form.cleaned_data['password']

        try:
            user = User.objects.get(username=student_id)
        except User.DoesNotExist:
            user = None

        if user:
            user = authenticate(username=user.username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
        messages.error(request, 'Invalid student ID or password')

    return render(request, 'core/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('welcome')

@login_required
def dashboard(request):
    positions = Position.objects.all()

    # Get the user's votes
    votes = Vote.objects.filter(user=request.user)
    voted_positions = votes.values_list('position_id', flat=True)

    # Create a dictionary to map position.id -> candidate.id the user voted for
    voted_candidates = {vote.position_id: vote.candidate_id for vote in votes}

    # Attach candidate list to each position manually to use in template
    for pos in positions:
        pos.candidates = Candidate.objects.filter(position=pos)

    return render(request, 'core/dashboard.html', {
        'positions': positions,
        'voted_candidates': voted_candidates,
        'voted_positions': voted_positions,
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