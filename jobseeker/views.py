from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404

from .forms import JobSeekerProfileForm, JobSeekerResumeForm
from .models import JobSeekerProfile, JobSeekerRequests, JobSeekerSaveJob
from employer.models import Job, JobRequests


def is_jobseeker(user):
    try:
        if not user.is_jobseeker:
            raise Http404
        return True
    except:
        raise Http404


@user_passes_test(is_jobseeker)
@login_required
def jobseeker_profile(request):
    JobSeekerProfile.objects.get_or_create(jobseeker=request.user)
    if request.method == 'POST':
        profile_form = JobSeekerProfileForm(
            request.POST,
            instance=request.user
        )
        resume_form = JobSeekerResumeForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        if profile_form.is_valid() and resume_form.is_valid():
            profile_form.save()
            resume_form.save()
            messages.success(request, 'Ваш профиль обновлен')
            return redirect('jobseeker-profile')
    else: 
        profile_form = JobSeekerProfileForm(instance=request.user)
        resume_form = JobSeekerResumeForm(
            instance=request.user.profile
        )
    context = {
        'profile_form' : profile_form,
        'resume_form' : resume_form,
    }
    return render(request, 'jobseeker_profile.html', context)


@login_required
@user_passes_test(is_jobseeker)
def request_job(request, id):
    if request.user.requests.filter(job=id):
        messages.warning(
            request,
            'Вы уже отправили свое резюме по этому объявлению.'
        )
        return redirect('home-page')
    if not request.user.profile.resume:
        messages.info(request, 'Сначала загрузите свое резюме.')
        return redirect('jobseeker-profile')
    job = get_object_or_404(Job, id=id)
    req = JobSeekerRequests(
        job=job,
        requests=request.user
    )
    req.save()
    req_to_employer = JobRequests(
        jobseeker=request.user,
        job=job,
        resume_url=request.user.profile.resume.url,
        employer=job.company,
        
    )
    req_to_employer.save()
    messages.success(request, 'Ваше резюме отправлено')
    return redirect('home-page')


@login_required
@user_passes_test(is_jobseeker)
def jobseeker_requests(request):
    requests = request.user.requests.all()
    if not requests:
        messages.info(request, 'Вы еще не отправили запрос')
    return render(request, 'jobseeker_requests.html', {'requests':requests})


@login_required
@user_passes_test(is_jobseeker)
def save_job(request, id):
    if request.user.saved_jobs.filter(job=id):
        messages.warning(request, 'Эта вакансия уже сохранена.')
        return redirect('home-page')
    job = get_object_or_404(Job, id=id)
    save_job = JobSeekerSaveJob(job=job, saved_job=request.user)
    save_job.save()
    messages.success(request, 'Вы сохранили вакансию')
    return redirect('home-page')


@login_required
@user_passes_test(is_jobseeker)
def jobseeker_saved_jobs(request):
    jobs = request.user.saved_jobs.all()
    return render(request, 'jobseeker_saved_jobs.html', {'jobs':jobs})


def cancel_request(request, id):
    jobseeker_req = get_object_or_404(request.user.requests, id=id)
    #request sent to employer
    if jobseeker_req.status != 'Подтверждено':
        jobseeker_req = request.user.requests.filter(id=id).delete()
        employer_req = JobRequests.objects.filter(id=id).delete()
        messages.success(request, 'Ваш запрос был отменен')
    else:
        raise Http404
    return redirect('jobseeker-requests')