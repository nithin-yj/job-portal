from django.urls import path
from .views import create_job, employer_jobs,job_detail,update_job,delete_job,job_list,employee_job_detail,apply_job
from .views import my_applications,job_applicants,employer_dashboard,employee_dashboard
from .views import update_application_status
from .views import view_resume, download_resume 




urlpatterns = [
    path(
        'create/',
        create_job,
        name='create_job'
    ),

    path(
        'my-jobs/',
        employer_jobs,
        name='employer_jobs'
    ),
    path(
    '<int:job_id>/',
    job_detail,
    name='job_detail'
    ),
    path(
    '<int:job_id>/edit/',
    update_job,
    name='update_job'
    ),
    path(
    '<int:job_id>/delete/',
    delete_job,
    name='delete_job'
    ),
    path(
    '',
    job_list,
    name='job_list'
    ),
    path('<int:job_id>/view/', employee_job_detail, name='employee_job_detail'),
    path(
    '<int:job_id>/apply/',
    apply_job,
    name='apply_job'
    ),
    path('my-applications/', my_applications, name='my_applications'),
    path(
    '<int:job_id>/applicants/',
    job_applicants,
    name='job_applicants'
    ),
    path(
    'employer-dashboard/',
    employer_dashboard,
    name='employer_dashboard'
    ),
    path(
    'employee-dashboard/',
    employee_dashboard,
    name='employee_dashboard'
    ),
    path(
    'applications/<int:application_id>/status/',
    update_application_status,
    name='update_application_status'
    ),
    path(
    'applications/<int:application_id>/resume/view/',
    view_resume,
    name='view_resume'
    ),
    path(
    'applications/<int:application_id>/resume/download/',
    download_resume,
    name='download_resume'
    ),
]