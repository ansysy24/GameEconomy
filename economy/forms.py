from django import forms
from django.utils.safestring import mark_safe

from economy.models import Commodity


class PlainTextWidget(forms.Widget):

    def render(self, name, value, attrs):
        return mark_safe(value) if value is not None else '-'


class CommodityPurchasingForm(forms.Form):
    suggested_price = forms.IntegerField(label='')
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super().__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['suggested_price'].required = False

