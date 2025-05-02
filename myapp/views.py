from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Item, Activity, UserProfile
from .forms import ItemForm, UserUpdateForm, ProfileUpdateForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('item_list')
        messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('item_list')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})

def home(request):
    return render(request, 'myapp/home.html')

@login_required
def item_list(request):
    items = Item.objects.filter(created_by=request.user)
    return render(request, 'myapp/item_list.html', {'items': items})

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            # Create activity log
            Activity.objects.create(
                user=request.user,
                action=f"Created item: {item.name}"
            )
            messages.success(request, "Item created successfully!")
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'myapp/item_form.html', {'form': form})

@login_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            Activity.objects.create(
                user=request.user,
                action=f"Updated item: {item.name}"
            )
            messages.success(request, "Item updated successfully!")
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'myapp/item_form.html', {'form': form})

@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        item_name = item.name
        item.delete()
        Activity.objects.create(
            user=request.user,
            action=f"Deleted item: {item_name}"
        )
        messages.success(request, "Item deleted successfully!")
        return redirect('item_list')
    return render(request, 'myapp/item_confirm_delete.html', {'item': item})

@login_required
def activity_feed(request):
    activities = Activity.objects.filter(user=request.user).order_by('-timestamp')[:20]
    return render(request, 'myapp/activity_feed.html', {'activities': activities})

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    activities = Activity.objects.filter(user=request.user).order_by('-created_at')[:10]
      
    return render(request, 'myapp/profile.html', {
        'profile': profile,
        'activities': activities
    })

@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            # Create activity log
            Activity.objects.create(
                user=request.user,
                action='PROFILE_UPDATE',
                details='Updated profile information'
            )
            
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    
    return render(request, 'myapp/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })