from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from .models import Commission, Comment, Job, JobApplication
from .forms import CommissionForm
from django.contrib.auth import get_user_model

User = get_user_model()

def commissions_list(request):
    commissions = Commission.objects.all().order_by('-status', '-created_on').values()
    JobApplication = JobApplication.objects.all()
    commissions_created = []
    commissions_applied = []
    if request.user.is_authenticated:
        commissions_created = commissions.filter(author=request.user.profile)
        commissions_applied = JobApplication.filter(author=request.user.profile)
    return render(request, '/commissions_list.html', {'commissions': commissions})

def commission_detail(request, pk):
    commission = get_object_or_404(Commission, pk=pk)
    job = Job.commission()
    manpower = Job.manpower_required()
    accepted_signees = JobApplication.filter(status='a')
    open_manpower = manpower - accepted_signees

    user_profile = getattr(user, 'profile', None)
    is_author = user.is_authenticated and commission.author == user_profile
    can_apply = user.is_authenticated and not is_author and manpower != accepted_signees
    
    form = JobApplicationForm()
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid() and can_apply:
            application = form.save(commit=False)
            application.applicant = user_profile
            application.job = job
            if manpower != accepted_signees:
                application.save()
                return redirect('commissions:commission_detail')

    return render(request, '/commission_detail.html', {'commission': commission, 'job': job, 'form': form, 'is_author': is_author, 'can_apply', can_apply})

@login_required
def commission_create(request):
    commission = Commission()
    fields = '__all__'
    form = CommissionForm()
    if request.method == "POST":
        form = CommissionForm(request.POST)
        if form.is_valid():
            comm = form.save(commit=False)
            comm.author = request.user.profile
            return redirect(request, '/commission_detail.html', pk = commission.pk)
    return render(request, '/commission_create.html', {'form': form})

@login_required
def commission_update(request, pk):
    commission = get_object_or_404(Commission, pk=pk)
    if commission.author != request.user.profile:
        return return redirect(request, '/commission_detail.html', pk = pk)
    form = CommissionForm()
    if request.method == "POST":
        form = CommissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request, '/commission_detail.html', pk = commission.pk)
    return render(request, '/commission_create.html', {'form': form, 'commission': commission})
