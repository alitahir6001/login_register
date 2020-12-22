from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt


# Create your views here.

def index(request):
    context = {
        'user': User.objects.all()
    }
    return render(request, "index.html", context)



def process(request):  # AKA registration process
    errors = User.objects.basic_validator(request.POST)
    
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    else:
        # add a user to the database

        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(pw_hash) # this will print the hashed pw in the console/shell
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
        request.session['logged_in'] = user.id
        return redirect('/success')

def login(request):  # AKA Login process
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['logged_in'] = user.id # creating a session, naming that session whatever we want.
        return redirect('/success')


def success(request):
    if "logged_in" not in request.session:  #if the user is not logged in
            return redirect('/')  #redirect back to the index
    else: 
        login = User.objects.get(id=request.session['logged_in'])
        context = {
            "logged_in": login,
            'user': User.objects.filter(email=request.session['logged_in'])
        }
    return render(request, 'success.html', context)

def logout(request):
    request.session.delete()
    return redirect('/')