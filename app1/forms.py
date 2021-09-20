from django import forms 
from .models import Inv_item,SOrder_item

from django.utils.translation import gettext_lazy as _

class InvItemForm(forms.ModelForm):
    class Meta:
        model= Inv_item
        fields= ["iprod","idist","iu","idd"] #'__all__'
        labels = {
            'iprod': _('Product'),
            'idist': _('Distributor'),
            'iu': _('Units'),
            'idd': _('Delivered date')
        }
        widgets = { 
            'idd': forms.SelectDateWidget,
        } 

class SOrderItemForm(forms.ModelForm):
    class Meta:
        model= SOrder_item
        fields= ["scust","sprod","sdisc"] #'__all__'
        labels = {
            'scust': _('Customer'),
            'sprod': _('Product'),
            'sdisc': _('Discount%')
        }
    
