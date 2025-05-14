from django.shortcuts import render
from .models import Commission, Comment, Job, JobApplication

def commissions_list(request):
    commissions = Commission.objects.all().order_by('-status', '-created_on').values()
    return render(request, 'commissions/commissions_list.html', {'commissions': commissions})

def commission_detail(request, commission_id):
    commission = get_object_or_404(Commission, id=commission_id), Job.objects.all()
    return render(request, 'commissions/commission_detail.html', {'commission': commission})

def detail(request):


@login_required
def create(request):

@login_required
def update(request):
