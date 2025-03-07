from django.shortcuts import render
from .models import Commission

def commissions_list(request):
    commissions = Commission.objects.all()
    return render(request, 'commissions/commissions_list.html', {'commissions': commissions})

def commission_detail(request, commission_id):
    article = get_object_or_404(Commission, id=commission_id)
    return render(request, 'commissions/commission_detail.html', {'commission': commission})
