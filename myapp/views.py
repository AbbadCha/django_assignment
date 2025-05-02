from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Item
from .forms import ItemForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('item_list')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'myapp/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
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
    items = Item.objects.all()
    return render(request, 'myapp/item_list.html', {'items': items})

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user  # Associate item with current user
            item.save()
            messages.success(request, "Item created successfully!")
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'myapp/item_form.html', {'form': form})

@login_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated successfully!")
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'myapp/item_form.html', {'form': form})

@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Item deleted successfully!")
        return redirect('item_list')
    return render(request, 'myapp/item_confirm_delete.html', {'item': item})