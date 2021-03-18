import random

import route53

from django.db import models, transaction
from django.contrib.auth.models import User
from django.conf import settings

from flags.state import (
    flag_state,
    flag_enabled,
    flag_disabled,
)

class AdvancedUser(User):
    initials = models.TextField(max_length=8, null=True, blank=True)
    subdomain = models.TextField(max_length=50)

class ProfileManager(models.Manager):

    def push_to_route53(self, profile, connection=None, subdomain_to_remove=None):
        """Pushes a new record to AWS route53. Removes an outdated record from AWS route53 if required."""
        if connection is None:
            connection = route53.connect(
                settings.AWS_ACCESS_KEY_ID,
                settings.AWS_SECRET_ACCESS_KEY,)

        for zone in connection.list_hosted_zones():
            if zone.name == f'{settings.DOMAIN}.':
                record_name = f'{profile.subdomain}.{settings.DOMAIN}.'
                records_names_set = set()

                if subdomain_to_remove:
                    for record_set in zone.record_sets:
                        records_names_set.add(record_set.name)
                        if record_set.name == f'{subdomain_to_remove}.{settings.DOMAIN}.':
                            record_set.delete()

                if record_name not in records_names_set:
                    zone.create_cname_record(
                        record_name,
                        values=[f'{settings.DOMAIN}'],
                        ttl=2800,
                    )

    def give_items(self, profile):
        from economy.models import Commodity
        for i in range(3):
            number = random.choices([0, 1, 2], weights=[0.2, 0.3, 0.5])[0]

            if number == 0:
                Commodity.objects.create(owner=profile, title='sword', on_the_market=False, price=20, sequence=i)
            if number == 1:
                Commodity.objects.create(owner=profile, title='stick', on_the_market=False, price=30, sequence=i)
            if number == 2:
                Commodity.objects.create(owner=profile, title='sand', on_the_market=False, price=50, sequence=i)

    def create(self, **obj_data):
        obj = super().create(**obj_data)
        if flag_enabled('PUSHING_SUBDOMAIN_TO_ROUTE53'):
            if obj.subdomain:
                self.push_to_route53(obj)
        if flag_enabled('GIVING_DEFAULT_ITEMS_WHEN_PROFILE_CREATED'):
            self.give_items(obj)
        return obj



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # type: User
    initials = models.TextField(max_length=8, null=True, blank=True)
    subdomain = models.TextField(max_length=50)
    show_messages = models.BooleanField(default=True)
    balance = models.IntegerField(default=100)
    balance_usd = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'

    def __repr__(self):
        return f'{self.user.username}'

    def put_on_market(self, sequence):
        from economy.models import Commodity, Purchase
        comm = Commodity.objects.get(owner=self, sequence=sequence)
        purchases = Purchase.objects.filter(commodity=comm)
        for purchase in purchases:
            purchase.commodity = None
            purchase.save()
        comm.on_the_market = True
        comm.save()
        Purchase.objects.create(seller=self, commodity=comm)
        return comm

    def get_market_items(self):
        from economy.models import Commodity, Purchase
        return Commodity.objects.filter(on_the_market=True, purchase__status=Purchase.STATUS.available).exclude(owner=self)

    def buy_commodity(self, commodity, price):
        from economy.models import Purchase
        if commodity.purchase.status == Purchase.STATUS.approved:
            from economy.models import Commodity
            with transaction.atomic():
                if self.balance >= price:
                    previous_owner = commodity.owner
                    previous_owner.balance += price
                    previous_owner.save()
                    self.balance = self.balance - price
                    self.save()
                    commodity.change_owner(self)
                    commodity.purchase.title = commodity.purchase.seller.user.username + '|' +\
                                               commodity.purchase.buyer.user.username + '|' + \
                                               commodity.title + '|' + str(commodity.purchase.final_price) + 'f'
                    commodity.purchase.save()
                    commodity.save()
                    return True
                else:
                    return False


    objects = ProfileManager()
