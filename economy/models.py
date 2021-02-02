from model_utils import Choices
from sorl.thumbnail import ImageField

from django.db import models

from users.models import Profile


class Commodity(models.Model):
    title = models.CharField(max_length=255)
    picture = ImageField(default='commodities_pics/default.jpg', upload_to='commodities_pics')
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    on_the_market = models.BooleanField(default=False)
    price = models.IntegerField(blank=True, null=True)
    sequence = models.IntegerField(blank=True, null=True)

    def change_owner(self, profile: Profile):
        # TODO explain
        self.owner = profile
        self.on_the_market = False
        commodities = Commodity.objects.filter(owner=profile)
        self.sequence = 0 if not commodities else commodities.order_by('-sequence')[0].sequence + 1
        self.purchase.status = Purchase.STATUS.done
        self.save()


class Purchase(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sales')
    buyer = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True, related_name='purchases')
    commodity = models.OneToOneField(Commodity, on_delete=models.SET_NULL, null=True)
    suggested_price = models.IntegerField(blank=True, null=True)
    final_price = models.IntegerField(blank=True, null=True)
    STATUS = Choices((0, 'available', 'AVAILABLE'),
                     (1, 'awaiting', 'AWAITING'),
                     (2, 'approved', 'APPROVED'),
                     (3, 'done', 'DONE'),
                     )
    status = models.SmallIntegerField(choices=STATUS, default=STATUS.available)
