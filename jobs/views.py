from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.http import FileResponse
from accounts.decorators import role_required
from accounts.models import User
from .forms import ApplicationForm, JobForm
from .models import Application, Job
from django.http import Http404



@role_required(User.Role.EMPLOYER)
def create_job(request):

    if request.method == 'POST':
        form = JobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()

            return redirect('employer_jobs')

    else:
        form = JobForm()

    return render(
        request,
        'create_job.html',
        {'form': form}
    )

@role_required(User.Role.EMPLOYER)
def employer_jobs(request):

    jobs = request.user.jobs.all()

    return render(
        request,
        'employer_jobs.html',
        {'jobs': jobs}
    )


@role_required(User.Role.EMPLOYER)
def job_detail(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=request.user
    )

    return render(
        request,
        'job_detail.html',
        {'job': job}
    )

@role_required(User.Role.EMPLOYER)
def update_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=request.user
    )

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)

        if form.is_valid():
            form.save()
            return redirect('job_detail', job_id=job.id)

    else:
        form = JobForm(instance=job)

    return render(
        request,
        'update_job.html',
        {'form': form, 'job': job}
    )


@role_required(User.Role.EMPLOYER)
def delete_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=request.user
    )

    if request.method == 'POST':
        job.delete()
        return redirect('employer_jobs')

    return render(
        request,
        'delete_job.html',
        {'job': job}
    )

@login_required
def job_list(request):
    search_query = request.GET.get('q', '').strip()

    jobs = Job.objects.filter(
        is_active=True
    ).order_by('-created_at')

    if search_query:
        jobs = jobs.filter(
            title__icontains=search_query
        )

    paginator = Paginator(jobs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'job_list.html',
        {
            'page_obj': page_obj,
            'search_query': search_query,
        }
    )

@login_required
def employee_job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)
    return render(request, 'employee_job_detail.html', {'job': job})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)

    if request.user.role != User.Role.EMPLOYEE:
        return redirect('home')

    if request.method == 'POST':

        if Application.objects.filter(
            employee=request.user,
            job=job
        ).exists():
            messages.warning(
                request,
                "You have already applied for this job."
            )
            return redirect(
                'employee_job_detail',
                job_id=job.id
            )

        form = ApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            application = form.save(commit=False)
            application.employee = request.user
            application.job = job
            application.save()

            messages.success(
                request,
                "Application submitted successfully."
            )

            return redirect(
                'employee_job_detail',
                job_id=job.id
            )

    else:
        form = ApplicationForm()

    return render(
        request,
        'apply_job.html',
        {
            'job': job,
            'form': form,
        }
    )
@login_required
def my_applications(request):
    if request.user.role != User.Role.EMPLOYEE:
        return redirect('home')

    applications = (
        Application.objects
        .filter(employee=request.user)
        .select_related('job')
        .order_by('-applied_at')
    )

    return render(
        request,
        'my_applications.html',
        {'applications': applications}
    )

@login_required
def job_applicants(request, job_id):
    if request.user.role != User.Role.EMPLOYER:
        return redirect('home')

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=request.user
    )

    applications = (
        Application.objects
        .filter(job=job)
        .select_related('employee')
        .order_by('-applied_at')
    )

    return render(
        request,
        'job_applicants.html',
        {
            'job': job,
            'applications': applications,
        }
    )


@login_required
def employer_dashboard(request):
    if request.user.role != User.Role.EMPLOYER:
        return redirect('home')

    jobs = Job.objects.filter(employer=request.user)

    total_jobs = jobs.count()
    active_jobs = jobs.filter(is_active=True).count()
    total_applications = Application.objects.filter(
        job__employer=request.user
    ).count()

    return render(
        request,
        'employer_dashboard.html',
        {
            'total_jobs': total_jobs,
            'active_jobs': active_jobs,
            'total_applications': total_applications,
        }
    )

@login_required
def employee_dashboard(request):
    if request.user.role != User.Role.EMPLOYEE:
        return redirect('home')

    applications = (
        Application.objects
        .filter(employee=request.user)
        .select_related('job')
        .order_by('-applied_at')
    )

    total_applications = applications.count()

    recent_applications = applications[:5]

    return render(
        request,
        'employee_dashboard.html',
        {
            'total_applications': total_applications,
            'recent_applications': recent_applications,
        }
    )

@login_required
def update_application_status(request, application_id):
    if request.user.role != User.Role.EMPLOYER:
        return redirect('home')

    application = get_object_or_404(
        Application,
        id=application_id,
        job__employer=request.user
    )

    if request.method == 'POST':
        new_status = request.POST.get('status')

        if new_status in ['APPLIED', 'SELECTED', 'REJECTED']:
            application.status = new_status
            application.save(update_fields=['status'])

        return redirect(
            'job_applicants',
            job_id=application.job.id
        )

    return redirect(
        'job_applicants',
        job_id=application.job.id
    )



@role_required(User.Role.EMPLOYER)
def view_resume(request, application_id):
    application = get_object_or_404(
        Application,
        id=application_id,
        job__employer=request.user
    )

    if not application.resume:
        raise Http404("Resume not found.")

    filename = application.resume.name.split('/')[-1]

    return FileResponse(
        application.resume.open('rb'),
        as_attachment=False,
        filename=filename,
        content_type='application/pdf'
    )


@role_required(User.Role.EMPLOYER)
def download_resume(request, application_id):
    application = get_object_or_404(
        Application,
        id=application_id,
        job__employer=request.user
    )

    if not application.resume:
        raise Http404("Resume not found.")

    filename = application.resume.name.split('/')[-1]

    return FileResponse(
        application.resume.open('rb'),
        as_attachment=True,
        filename=filename,
        content_type='application/pdf'
    )