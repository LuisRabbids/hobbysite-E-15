from django.shortcuts import render
from .models import Commission, Comment, Job, JobApplication
from .forms import CommissionForm

User = get_user_model()

def commissions_list(request):
    commissions = Commission.objects.all().order_by('-status', '-created_on').values()
    if request.method == "POST":
        c = Commission()
        c.created = request.POST.get('title')
        ja = JobApplication()
        ja.applied = request.POST.get('job')
    return render(request, 'commissions/commissions_list.html', {'commissions': commissions})

def commission_detail(request, commission_id):
    commission = get_object_or_404(Commission, id=commission_id)
    jobs = Job.objects.all()
    #manpower
    #apply to job
    #jobapp entries
    #logged in user
    return render(request, 'commissions/commission_detail.html', {'commission': commission})

@login_required
def commission_create(request):
    model = Commission()
    fields = '__all__'
    form = CommissionForm()
    if request.method == "POST":
        form = CommissionForm(request.POST)
        if form.is_valid():
            comm = form.save(commit=False)
            comm.author = request.user.profile

@login_required
def commission_update(request):
    model = Commission()
    fields = '__all__'
    template_name = 'commission_detail.html'
    form = CommissionForm