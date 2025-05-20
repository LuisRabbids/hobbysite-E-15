from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Case, When, Value, IntegerField, Prefetch, Exists, OuterRef, Sum, Count, Q, F # <--- ADDED Q and F HERE
from django.forms import inlineformset_factory
from django.contrib import messages
from .models import Commission, Job, JobApplication
from .forms import CommissionForm, JobFormSet, JobApplicationForm, JobApplicationUpdateForm
from user_management.models import Profile # Ensure this import is correct

@login_required
def commission_create(request):
    if request.method == "POST":
        form = CommissionForm(request.POST)
        job_formset = JobFormSet(request.POST, prefix='jobs')
        if form.is_valid() and job_formset.is_valid():
            commission = form.save(commit=False)
            commission.author = request.user.profile
            commission.save()
            
            job_formset.instance = commission
            job_formset.save()
            
            messages.success(request, "Commission created successfully!")
            return redirect(reverse('commissions:commission_detail', kwargs={'pk': commission.pk}))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CommissionForm()
        job_formset = JobFormSet(prefix='jobs')

    return render(request, 'commissions/commission_form.html', {
        'form': form,
        'job_formset': job_formset,
        'form_title': 'Create New Commission'
    })

@login_required
def commission_update(request, pk):
    commission = get_object_or_404(Commission, pk=pk)

    if commission.author != request.user.profile:
        messages.error(request, "You are not authorized to edit this commission.")
        return redirect(reverse('commissions:commission_detail', kwargs={'pk': commission.pk}))

    if request.method == "POST":
        form = CommissionForm(request.POST, instance=commission)
        job_formset = JobFormSet(request.POST, instance=commission, prefix='jobs')

        if form.is_valid() and job_formset.is_valid():
            updated_commission = form.save()
            job_formset.save()

            # Update commission status if all jobs are full
            all_jobs_full = True
            active_jobs = updated_commission.jobs.all()
            if not active_jobs.exists(): # No jobs means not "Full" by jobs
                 all_jobs_full = False
            else:
                for job in active_jobs:
                    job.update_status_if_full() # Ensure individual job statuses are current
                    if job.status != Job.FULL:
                        all_jobs_full = False
                        # No need to break, let all jobs update their status
            
            if all_jobs_full and updated_commission.status != Commission.FULL and updated_commission.status not in [Commission.COMPLETED, Commission.DISCONTINUED]:
                updated_commission.status = Commission.FULL
                updated_commission.save(update_fields=['status', 'updated_on'])
            elif not all_jobs_full and updated_commission.status == Commission.FULL and updated_commission.status not in [Commission.COMPLETED, Commission.DISCONTINUED] :
                 updated_commission.status = Commission.OPEN
                 updated_commission.save(update_fields=['status', 'updated_on'])


            messages.success(request, "Commission updated successfully!")
            return redirect(reverse('commissions:commission_detail', kwargs={'pk': updated_commission.pk}))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CommissionForm(instance=commission)
        job_formset = JobFormSet(instance=commission, prefix='jobs')

    return render(request, 'commissions/commission_form.html', {
        'form': form,
        'job_formset': job_formset,
        'commission': commission,
        'form_title': f'Update Commission: {commission.title}'
    })

def commissions_list(request):
    status_order = Case(
        When(status=Commission.OPEN, then=Value(1)),
        When(status=Commission.FULL, then=Value(2)),
        When(status=Commission.COMPLETED, then=Value(3)),
        When(status=Commission.DISCONTINUED, then=Value(4)),
        default=Value(5),
        output_field=IntegerField()
    )
    all_commissions = Commission.objects.annotate(custom_status_order=status_order)\
                                    .order_by('custom_status_order', '-created_on')\
                                    .select_related('author__user')

    commissions_created = None
    commissions_applied_to = None

    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)
        if profile:
            commissions_created = all_commissions.filter(author=profile)
            
            applied_commission_ids = JobApplication.objects.filter(applicant=profile)\
                                                           .values_list('job__commission_id', flat=True)\
                                                           .distinct()
            commissions_applied_to = all_commissions.filter(id__in=applied_commission_ids)
                                                    
    context = {
        'all_commissions': all_commissions,
        'commissions_created': commissions_created,
        'commissions_applied_to': commissions_applied_to,
    }
    return render(request, 'commissions/commission_list.html', context)


def commission_detail(request, pk):
    commission = get_object_or_404(Commission.objects.select_related('author__user'), pk=pk)
    
    jobs_with_details = commission.jobs.annotate(
        accepted_count=Count('applications', filter=Q(applications__status=JobApplication.ACCEPTED))
    ).annotate(
        open_manpower_slots=F('manpower_required') - F('accepted_count')
    ).all()

    user_profile = getattr(request.user, 'profile', None)
    is_author = request.user.is_authenticated and commission.author == user_profile

    job_application_form = JobApplicationForm()

    if request.method == 'POST' and 'apply_job_id' in request.POST and request.user.is_authenticated and user_profile and not is_author:
        job_id_to_apply = request.POST.get('apply_job_id')
        job_to_apply = get_object_or_404(Job, pk=job_id_to_apply, commission=commission)

        if job_to_apply.is_full() or job_to_apply.status == Job.FULL:
            messages.error(request, f"The job '{job_to_apply.role}' is already full.")
        elif JobApplication.objects.filter(job=job_to_apply, applicant=user_profile).exists():
            messages.warning(request, f"You have already applied for the job '{job_to_apply.role}'.")
        else:
            application = JobApplication(job=job_to_apply, applicant=user_profile)
            # Default status is PENDING, so no need to set it explicitly unless specified otherwise
            application.save()
            
            # Check if job became full AFTER this application if status was auto-accepted
            # For now, with PENDING default, only admin action makes it full.
            # But let's call update_status_if_full in case rules change (e.g. auto-accept)
            # or if manual DB changes make it full.
            # For applications, the owner will accept them. This logic mostly for owner's view.
            # The job's own update_status_if_full() will be key when applications are accepted.

            messages.success(request, f"Successfully applied for the job '{job_to_apply.role}'. Your application is pending.")
            return redirect(reverse('commissions:commission_detail', kwargs={'pk': commission.pk}))
    
    applications_for_commission = None
    application_update_forms = {}
    if is_author:
        applications_for_commission = JobApplication.objects.filter(job__commission=commission)\
                                                            .select_related('applicant__user', 'job')\
                                                            .order_by('job__role', 'status', '-applied_on')
        
        if request.method == 'POST' and 'update_application_id' in request.POST:
            app_id = request.POST.get('update_application_id')
            application_to_update = get_object_or_404(JobApplication, pk=app_id, job__commission=commission)
            # Pass prefix when instantiating form for POST data
            app_update_form = JobApplicationUpdateForm(request.POST, instance=application_to_update, prefix=f"app_{app_id}")

            if app_update_form.is_valid():
                original_status = application_to_update.status
                updated_app = app_update_form.save()
                messages.success(request, f"Application status for {updated_app.applicant.user.username if updated_app.applicant.user else updated_app.applicant} updated to {updated_app.get_status_display()}.")
                
                job_affected = updated_app.job
                # Call update_status_if_full on the job, which now considers the new application status
                job_status_changed = job_affected.update_status_if_full()

                # If job became open again (e.g. an 'Accepted' was changed to 'Rejected' or 'Pending')
                if job_affected.status == Job.OPEN and job_status_changed and commission.status == Commission.FULL \
                   and commission.status not in [Commission.COMPLETED, Commission.DISCONTINUED]:
                    commission.status = Commission.OPEN
                    commission.save(update_fields=['status', 'updated_on'])
                    messages.info(request, f"Commission '{commission.title}' status set to Open as job '{job_affected.role}' has open slots.")
                # If job became full
                elif job_affected.status == Job.FULL and job_status_changed:
                    all_commission_jobs_full = True
                    active_jobs_for_commission = commission.jobs.all()
                    if not active_jobs_for_commission.exists():
                        all_commission_jobs_full = False
                    else:
                        for j_instance in active_jobs_for_commission:
                            if j_instance.status != Job.FULL: # Check current status from DB
                                all_commission_jobs_full = False
                                break
                    if all_commission_jobs_full and commission.status != Commission.FULL and commission.status not in [Commission.COMPLETED, Commission.DISCONTINUED]:
                        commission.status = Commission.FULL
                        commission.save(update_fields=['status', 'updated_on'])
                        messages.info(request, f"Commission '{commission.title}' status set to Full as all its jobs are now full.")
                
                return redirect(reverse('commissions:commission_detail', kwargs={'pk': commission.pk}))
            else:
                # If form is invalid, ensure it's passed back to the template with errors
                application_update_forms[application_to_update.id] = app_update_form
                messages.error(request, f"Error updating application status for {application_to_update.applicant.user.username if application_to_update.applicant.user else application_to_update.applicant}. Please check the form.")


        for app in applications_for_commission:
            if app.id not in application_update_forms: # Don't overwrite a form that had errors from POST
                application_update_forms[app.id] = JobApplicationUpdateForm(instance=app, prefix=f"app_{app.id}")


    detailed_jobs_for_template = []
    for job_instance in jobs_with_details:
        user_application_status = None
        can_apply_to_job = False # Renamed for clarity
        if request.user.is_authenticated and user_profile and not is_author:
            existing_app = JobApplication.objects.filter(job=job_instance, applicant=user_profile).first()
            if existing_app:
                user_application_status = existing_app.get_status_display()
            # Check open_manpower_slots (which is job.manpower_required - job.accepted_count)
            if not existing_app and job_instance.open_manpower_slots > 0 and job_instance.status == Job.OPEN:
                can_apply_to_job = True
        
        detailed_jobs_for_template.append({
            'job': job_instance, # Contains .role, .manpower_required, .status, .accepted_count, .open_manpower_slots
            'user_application_status': user_application_status,
            'can_apply': can_apply_to_job, # Use this in template
            'is_job_full_display': job_instance.open_manpower_slots <= 0 or job_instance.status == Job.FULL
        })

    context = {
        'commission': commission,
        'jobs_for_template': detailed_jobs_for_template,
        'total_manpower': commission.get_total_manpower_required(),
        'open_manpower': commission.get_open_manpower(),
        'is_author': is_author,
        'job_application_form': job_application_form, # For non-authors to apply
        'applications_for_commission': applications_for_commission, # For owner to manage
        'application_update_forms': application_update_forms, # For owner to manage
    }
    return render(request, 'commissions/commission_detail.html', context)