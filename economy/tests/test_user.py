from django.test import TestCase
from django.contrib.auth.models import User

from economy.models import Commodity
from users.models import Profile


class UserTestCase(TestCase):

    def test_two_users_created_and_got_random_items(self):
        admin = User.objects.create_superuser('admin', 'admin@admin.com', 'password')

        user1 = User.objects.create_user('user1', 'user1@gmail.com', 'password')
        profile1 = Profile.objects.create(user=user1, domain='user1', balance=1, balance_usd=1)

        user2 = User.objects.create_user('user2', 'user2@gmail.com', 'password')
        profile2 = Profile.objects.create(user=user2, domain='user2', balance=2, balance_usd=2)

        self.assertEqual(Commodity.objects.filter(owner=profile1).count(), 3)
        self.assertEqual(Commodity.objects.filter(owner=profile2).count(), 3)

    def test_user_puts_his_commodities_on_market(self):
        admin = User.objects.create_superuser('admin', 'admin@admin.com', 'password')

        user1 = User.objects.create_user('user1', 'user1@gmail.com', 'password')
        profile1 = Profile.objects.create(user=user1, domain='user1', balance=1, balance_usd=1)
        profile1.put_on_market(0)

        user2 = User.objects.create_user('user2', 'user2@gmail.com', 'password')
        profile2 = Profile.objects.create(user=user2, domain='user2', balance=2, balance_usd=2)


        self.assertEqual(profile2.get_market_items()[0], Commodity.objects.get(owner=profile1, sequence=0))

    def test_user1_selling_commodity_to_user2(self):
        admin = User.objects.create_superuser('admin', 'admin@admin.com', 'password')

        user1 = User.objects.create_user('user1', 'user1@gmail.com', 'password')
        profile1 = Profile.objects.create(user=user1, domain='user1', balance=100, balance_usd=1)
        profile1.put_on_market(0)


        user2 = User.objects.create_user('user2', 'user2@gmail.com', 'password')
        profile2 = Profile.objects.create(user=user2, domain='user2', balance=100, balance_usd=2)
        commodity = profile2.get_market_items()[0]
        self.assertEqual(commodity.owner, profile1)

        purchase = profile2.buy_commodity(commodity, commodity.price)

        profile2.refresh_from_db()
        profile1.refresh_from_db()
        commodity.refresh_from_db()

        self.assertEqual(purchase, True)
        self.assertEqual(commodity.owner, profile2)
        self.assertEqual(profile2.balance, 100 - commodity.price)
        self.assertEqual(profile1.balance, 100 + commodity.price)
