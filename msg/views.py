from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Message
from .forms import MessageForm, SignupForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms


def home(request):
    # TODO: Criar login required e melhorar essa exibição.
    msgs = Message.objects.all().order_by('-created_at')

    if request.user.is_authenticated:
        
        form = MessageForm(request.POST or None)

        if request.method == "POST":
            if form.is_valid():
                msg = form.save(commit=False)
                msg.user = request.user
                msg.save()

                messages.success(request, 'Postado com sucesso.')
                return redirect('home')
        
        return render(request, 'home.html', {'msgs': msgs, 'form': form})
    else:
        return render(request, 'home.html', {'msgs': msgs})

# TODO: Criar um login required
def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {'profiles': profiles})
    else:
        messages.success(request, 'Você precisa estar logado para visualizar está página.')
        return redirect('home')
    

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        msgs = Message.objects.filter(user_id=pk).order_by('-created_at')

        # Post form Logic
        if request.method == "POST":
            # Get current user ID
            current_user_profile = request.user.profile
            # Get form date
            action = request.POST['follow']
            # Decide to follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)

            # Save the profile
            current_user_profile.save()

        return render(request, 'profile.html', {'profile': profile, 'msgs': msgs})

    else:
        messages.success(request, 'Você precisa estar logado para visualizar está página.')

        return redirect('home')
    
def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            messages.success(request, 'Login efetuado com sucesso.')

            return redirect('home')
        
        else:
            messages.success(request, 'Algum erro ocorreu. Tente novamente.')

            return redirect('login_page')
    else:
        return render(request, 'login.html')

def logout_page(request):
    logout(request)

    messages.success(request, 'Você saiu.')

    return redirect('home')

def register_page(request):
    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, 'Logou com sucesso.')
            return redirect('home')

    return render(request, 'register.html', {'form': form})
