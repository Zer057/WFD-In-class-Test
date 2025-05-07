from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    users = User.objects.all()
    total_users = users.count()
    total_candidates = candidates.count()

    context = {
        'users': users,
        'candidates': candidates,
        'total_users': total_users,
        'total_candidates': total_candidates,
    }
    return render(request, 'recruitment/admin_dashboard.html', context)
