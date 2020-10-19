from django.test import TestCase
from django.contrib.auth.models import User

from economy.models import Commodity

class AdminTestCase(TestCase):

    def test_admin_user_add_3_types_of_commodities(self):
        admin = User.objects.create_superuser('admin', 'admin@admin.com', 'password')
        comm1 = Commodity.objects.create(title='comm1', price=1)
        comm2 = Commodity.objects.create(title='comm2', price=2)
        comm3 = Commodity.objects.create(title='comm3', price=3)

        self.assertEqual(comm1.title, 'comm1')
        self.assertEqual(comm1.owner, None)
        self.assertEqual(comm1.on_the_market, False)

    
