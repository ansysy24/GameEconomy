from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from users.forms import UserRegisterForm
from economy.models import Commodity, Purchase


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request, **kwargs):
    context = {'commodities': Commodity.objects.filter(owner=request.user.profile)}
    template = 'users/profile.html'
    if 'pk' in kwargs and request.method == 'GET':
        context['public_user'] = User.objects.get(id=int(kwargs['pk']))
        context['commodities'] = Commodity.objects.filter(owner=context['public_user'].profile)
        template = 'users/public_profile.html'

    if request.method == 'POST':
        submit = request.POST.get('submit')
        if 'Change' in submit:
            request.user.email = request.POST.get('email')
            request.user.save()
            request.user.profile.initials = request.POST.get('initials')
            request.user.profile.show_messages = bool(request.POST.get('show_messages'))
            request.user.profile.save()
            new_subdomain = request.POST.get('subdomain')
            if new_subdomain and request.user.profile.subdomain != new_subdomain:
                subdomain_to_remove = request.user.profile.subdomain
                request.user.profile.subdomain = new_subdomain
                request.user.profile.save()
                # Profile.objects.push_to_route53(request.user.profile, subdomain_to_remove=subdomain_to_remove)

        elif 'Put' in submit:
            comm_ids = request.POST.getlist('selected_items[]')
            for id in comm_ids:
                comm = Commodity.objects.get(id=int(id))
                request.user.profile.put_on_market(comm.sequence)

        elif 'Withdraw' in submit:
            comm_id = int(submit.split('-')[-1])
            comm = Commodity.objects.get(id=comm_id)
            comm.on_the_market = False
            comm.save()

        elif 'Approve' in submit or 'Cancel' in submit:
            comm_id = int(submit.split('-')[-1])
            comm = Commodity.objects.get(id=comm_id)
            if 'Approve' in submit:
                comm.purchase.status = Purchase.STATUS.approved
                comm.purchase.save()
                comm.purchase.buyer.buy_commodity(comm, comm.purchase.suggested_price)
            else:
                comm.purchase.status = Purchase.STATUS.available
                comm.purchase.suggested_price = None
                comm.purchase.save()

        elif 'Set' in submit:
            comm_id = int(submit.split('-')[-1])
            comm = Commodity.objects.get(id=comm_id)
            comm.price = int(request.POST.get('new_price'))
            comm.save()

    return render(request, template, context)

@login_required
def users_list(request):
    return render(request, 'users/users_list.html', {'users': User.objects.all().exclude(id=request.user.id)})
