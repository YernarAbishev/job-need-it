from datetime import datetime, timezone

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import Http404

from employer.models import Job
from jobseeker.models import JobSeekerRequests
from .forms import UserRegisterForm, UserLoginForm
from .models import User

def banner_page(request):
    return render(request, "banner.html")

def home_page(request):
    jobs = Job.objects.order_by('-created_date').all()
    now = datetime.now(timezone.utc)
    for i in jobs:
        get_days = now - i.created_date
        if get_days.days > 1:
            i.created_date = f'{get_days.days} дней'
    return render(request, 'home_page.html', {'jobs':jobs})


def job_detail(request, id):
    job = get_object_or_404(Job, id=id)
    return render(request, 'job_detail.html', {'job':job})


def employer_register(request):
    if request.user.is_authenticated:
            raise Http404
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                    data['email'],
                    data['full_name'],
                    data['password1'],
            )
            user.is_jobseeker = False
            user.save()
            messages.success(
                request, 'Регистрация прошла успешно! Пройдите авторизацию'
            )
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'employer/register.html', {'form':form})


def jobseeker_register(request):
    if request.user.is_authenticated:
            raise Http404
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                    data['email'],
                    data['full_name'],
                    data['password1'],
            )
            user.save()
            messages.success(
                request, 'Регистрация прошла успешно! Пройдите авторизацию'
            )
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'jobseeker/register.html', {'form':form})


def login_request(request):
    if request.user.is_authenticated:
        raise Http404
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, email=data['email'], password=data['password']
            )
            if user is not None:
                login(request, user)
                if user.is_jobseeker:
                    return redirect('home-page')
                elif not user.is_jobseeker:
                    return redirect('employer-home')
            else:
                messages.success(request, 'Неправильный логин или пароль')
                return redirect('login')
    form = UserLoginForm()
    return render(request, 'login.html', {'form':form})



def search(request):
    query = request.GET.get('q')
    resaults =  Job.objects.filter(title__icontains=query).all()
    now = datetime.now(timezone.utc)
    for i in resaults:
        get_days = now - i.created_date
        if get_days.days > 1:
            i.created_date = f'{get_days.days} дней'
    return render(request, 'home_page.html', {'jobs':resaults})


def filter_by_category(request, category):
    resaults = Job.objects.filter(category__name=category).all()
    now = datetime.now(timezone.utc)
    for i in resaults:
        get_days = now - i.created_date
        if get_days.days > 1:
            i.created_date = f'{get_days.days} дней'
    return render(request, 'home_page.html', {'jobs':resaults})