import time

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.forms import formset_factory
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache

from economy.forms import CommodityPurchasingForm
from economy.models import Commodity, Purchase
from users.models import Profile

events = dict()  # key: username # value: list of 'winner' strings


@login_required(login_url='/login')
def home(request):
    context = {'commodities': Commodity.objects.filter(owner=request.user.profile),
               }
    if request.method == 'GET':
        return render(request, 'economy/home.html', context)





@login_required(login_url='/login')
def market_view(request):

    # TODO use django forms and create class view
    if request.method == 'POST':
        suggested_price = request.POST.get('suggested_price')
        comm = request.POST.get('comm')
        comm_id = comm.split('-')[-1]
        commodity = Commodity.objects.get(id=int(comm_id))
        price = commodity.price
        if suggested_price:
            price = suggested_price
            commodity.purchase.suggested_price = suggested_price
            commodity.purchase.status = Purchase.STATUS.awaiting
        else:
            commodity.purchase.status = Purchase.STATUS.approved
            # TODO make sure what line is more important
            commodity.purchase.save()
            commodity.save()
            request.user.profile.buy_commodity(commodity, price)
        commodity.purchase.buyer = request.user.profile
        commodity.purchase.final_price = price
        commodity.purchase.save()
        commodity.save()

    # CommodityPurchasingFormSet = inlineformset_factory(Profile, Commodity, form=CommodityPurchasingForm, can_delete=False)
    CommodityFormSet = formset_factory(CommodityPurchasingForm)

    owners = Profile.objects.exclude(user=request.user)

    # owner_formsets = [CommodityPurchasingFormSet(instance=owner) for owner in owners]

    context = {'commodities': request.user.profile.get_market_items(), 'formsets': CommodityFormSet}
    return render(request, 'economy/market.html', context)


class PurchasesListView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'economy/purchases.html'
    paginate_by = 30

    def get_queryset(self):
        qs = super().get_queryset()
        title = self.request.GET.get('title_search')
        qs = qs.filter(status=Purchase.STATUS.done)
        # qs = qs.filter(title__contains=title)
        return qs


@login_required(login_url='/login')
def long_polling_view(request):
    while True:
        keys = cache.keys('winner:*')
        for target, balance in cache.get_many(keys).items():
            cache.delete(target)
            _, profile_id = target.split(':')
            if request.user.profile.id == int(profile_id):
                return JsonResponse({'type': 'reload', 'balance': balance})
            else:
                return JsonResponse({'type': 'reload', 'balance': ''})
        time.sleep(1)


@login_required(login_url='/login')
def models_view(request):
    return render(request, 'economy/models.html')


@login_required(login_url='/login')
def market_use_cases(request):
    return render(request, 'economy/market_use_case.html')


def stopwatch_view(request):
    return render(request, 'economy/stopwatch.js', content_type='application/x-javascript')
