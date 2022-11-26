from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Place, Rating


@login_required(login_url='user_login')
def writer_page(request, pk):
    place = Place.objects.filter(user=pk)
    
    if request.method == 'POST':
        user = request.POST.get('user')
        title = request.POST.get('title')
        description = request.POST.get('description')
        imageUrl = request.POST.get('imageUrl')
        
        # user
        place_d = request.POST.get('place_d')
        
        if user and title and description and imageUrl is not None:
            Place.objects.create(
                user=User.objects.get(id=user),
                title=title,
                description=description,
                imageUrl=imageUrl
            )
            return redirect('writer', pk=pk)
        elif Place.objects.filter(id=place_d, user=User.objects.get(id=user)) and user and place_d is not None:
            place_delete = Place.objects.get(id=place_d)
            place_delete.delete()
            return redirect('writer', pk=pk)
        else:
            return redirect('writer', pk=pk)
    
    vars = {
        'place': place
    }
    return render(request, 'writer.html', vars)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        email = request.POST.get('email')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        # password
        confpassword = request.POST.get('confpassword')
        user_login = authenticate(request, username=username, password=password)
        
        if user_login is not None:
            login(request, user_login)
            return redirect('home')
        elif user_login is None and password == confpassword:
            user_register = User.objects.create_user(
                username=email,
                password=password,
                email=email,
                first_name=fname,
                last_name=lname,
            )
            login(request, user_register)
            return redirect('home')
        else:
            return redirect('user_login')

    return render(request, 'login.html')


def log_user_out(request):
    logout(request)
    return redirect('home')


def home(request):
    place = Place.objects.filter(active=True).order_by('-updated')
    vars = {
        'place': place
    }
    return render(request, 'home.html', vars)


def place_details(request, pk):
    place = Place.objects.get(id=pk)
    review = Rating.objects.filter(place=pk).order_by('-created')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        stars = request.POST.get('stars')
        comment = request.POST.get('comment')
        # print(username, stars, comment)
        
        if Rating.objects.filter(place=place, user=User.objects.get(id=username)).exists():
            messages.success(request, 'You have already comment !') 
            return redirect('place_details', pk=pk)
        else:
            Rating.objects.create(
                place=place,
                user=User.objects.get(id=username),
                stars=stars,
                comment=comment
            )
            return redirect('place_details', pk=pk)
    
    vars = {
        'place': place,
        'review': review
    }
    
    return render(request, 'place_details.html', vars)