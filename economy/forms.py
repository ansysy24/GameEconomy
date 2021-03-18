from django import forms
from django.utils.safestring import mark_safe

from economy.models import Commodity


class PlainTextWidget(forms.Widget):

    def render(self, name, value, attrs):
        return mark_safe(value) if value is not None else '-'


class CommodityPurchasingForm(forms.Form):
    new_price = forms.IntegerField(label='suggest your price ')
    class Meta:
        exclude = ()
