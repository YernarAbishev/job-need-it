from datetime import datetime, timezone

from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

from .forms import EmployerJobCreationForm, EmployerProfileForm
from .models import Company, JobRequests


def is_employer(user):
    try:
        if user.is_jobseeker:
            raise Http404
        return True
    except:
        raise Http404


@user_passes_test(is_employer)
@login_required
def employer_home(request):
    try:
        requests = JobRequests.objects.filter(
            employer=request.user.company, accepted=False
            ).all()
        accepted_requests = JobRequests.objects.filter(
            employer=request.user.company, accepted=True
            ).all()
    except Company.DoesNotExist:
        messages.success(
            request,
            'Чтобы получить доступ к другим разделам, сначала заполните следующую информацию.'
        )
        return redirect('employer-profile')
    context = {
        'requests':requests,
        'accepted_requests': accepted_requests,
        }
    return render(request, 'employer_home.html', context)


@user_passes_test(is_employer)
@login_required
def employer_profile(request):
    try:
        if request.method == 'POST':
            form = EmployerProfileForm(
                request.POST, request.FILES, instance=request.user.company
                )
            if form.is_valid():
                instance = form.save(commit=False)
                instance.employer = request.user
                instance.save()
                messages.success(request, 'Ваш профиль был обновлен.')
                return redirect('employer-profile')
        form = EmployerProfileForm(instance=request.user.company)
    except Company.DoesNotExist:
            # if user is new and has not a profile
            if request.method == 'POST':
                form = EmployerProfileForm(request.POST)
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.employer = request.user
                    instance.save()
                    messages.success(request, 'Ваш профиль создан')
                    messages.success(request, 'Чтобы создать вакансию, выберите новый вариант объявления в верхнем меню.')
                    return redirect('employer-profile')
            form = EmployerProfileForm()
    return render(request, 'profile.html', {'form':form})


@user_passes_test(is_employer)
@login_required
def employer_jobs(request):
    try:
        jobs = request.user.company.jobs.all()
        now = datetime.now(timezone.utc)
        for i in jobs:
            get_days = now - i.created_date
            if get_days.days > 1:
                i.created_date = f'{get_days.days} дней'
        requests = JobRequests.objects.filter(employer=request.user.company)
    except Company.DoesNotExist:
        return redirect('employer-home')
    return render(request, 'jobs.html', {'jobs':jobs, 'number':len(requests)})


@user_passes_test(is_employer)
@login_required
def employer_create_job(request):
    """ create a job and publishe it to the portal"""
    try:
        if request.method == 'POST':
            form = EmployerJobCreationForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.company = request.user.company
                instance.save()
                messages.success(request, 'Ваше вакансия опубликована')
                return redirect('job-detail', id=instance.id)
        elif request.method == 'GET':
            form = EmployerJobCreationForm()
    except Company.DoesNotExist:
        raise Http404
    return render(request, 'create_job.html', {'form':form})


def accepted_status(request, id):
    req = JobRequests.objects.filter(id=id).first()
    req.accepted = True
    req.save()
    return redirect('employer-home')


def hired_status(request, id):
    req = JobRequests.objects.filter(id=id).first()
    req.hired = True
    return redirect('employer-home')


def delete_request(request, id):
    req = JobRequests.objects.filter(id=id).delete()
    return redirect('employer-home')