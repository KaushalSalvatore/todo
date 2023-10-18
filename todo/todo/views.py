from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from todo.models import TODOO
from django.contrib.auth import authenticate,login as auth_login,logout,user_logged_in,user_logged_out
from django.contrib.auth.decorators import login_required
from django.contrib import messages




def signup(request):
    if request.method=='POST':
        name = request.POST.get('fnm')
        email = request.POST.get('emailid')
        password = request.POST.get('pwd')

        if User.objects.filter(username = name).first():
            messages.error(request, "This username is already taken")
            return redirect('/')

        user = User.objects.create_user(name,email,password)
        user.save()
        return redirect('/login')
    return render(request,'signup.html')

def login(request):
    if request.method == 'POST':
        name = request.POST.get('fnm')
        password = request.POST.get('pwd')
        print(name,password)
        user = authenticate(request,username=name,password=password)
        if user is not None:
            auth_login(request,user)
            return redirect('/todo')
        else:
            print("somthing wend wrong")
            return redirect('/login')

    return render(request,'login.html')

@login_required(login_url='/login')    
def todo(request):
    if request.method=='POST':
        title=request.POST.get('title')
        data= TODOO(title=title,user=request.user)
        data.save()
        res=TODOO.objects.filter(user=request.user).order_by('date')
        return redirect('/todo',{'res':res})
    res=TODOO.objects.filter(user=request.user).order_by('date')
    return render(request,'todo.html',{'res':res})


@login_required(login_url='/login')
def edit_todo(request,srno):
    if request.method=='POST':
        title=request.POST.get('title')

        data= TODOO.objects.get(srno=srno)
        data.title=title
        data.save()
        return redirect('/todo')

    data= TODOO.objects.get(srno=srno)
    return render(request, 'edit_todo.html', {'data': data})

@login_required(login_url='/login')
def delete_todo(request,srno):
    print(srno)
    obj=TODOO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todo')

def signout(request):
    logout(request)
    return redirect('/login')