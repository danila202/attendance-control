from django import forms


class SubscriptionForm(forms.Form):
    subscription_id = forms.CharField(label='Номер абонемента', max_length=1000)
