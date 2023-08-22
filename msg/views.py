from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Message
from .forms import MessageForm


def home(request):
    if request.user.is_authenticated:
        msgs = Message.objects.all().order_by('-created_at')
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
