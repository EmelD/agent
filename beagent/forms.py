# coding: utf-8

from django.db.models import Q
from django import forms
from beagent.models import USER_TYPE, User, MoneyTransfer, NonCashPayment, AgentPurse, PAYMENT_SYSTEM_CHOICES, MessageReview

class SignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=6, max_length=32)

class SignUpForm(SignInForm):
    type = forms.TypedChoiceField(choices=USER_TYPE)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(u'E-mail уже используется.')

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('date_added','rating','type','is_staff','password','last_login','email','balance',)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.filter(email=email).exclude(pk=self.initial['user'])[0]
        except IndexError:
            return email
        raise forms.ValidationError('Email already in use.')

class PasswordForm(forms.Form):
    pass

class DateForm(forms.Form):
    date_from = forms.DateField()
    date_to = forms.DateField()

class PurseForm(forms.Form):
    name = forms.CharField(max_length=20)

class PaymentsForm(forms.Form):
    class Meta:
        model = MoneyTransfer
        exclude = ('status','total_sum')

class NonCashPaymentsForm(forms.ModelForm):
    class Meta:
        model = NonCashPayment

class MessageReviewForm(forms.ModelForm):
    class Meta:
        model = MessageReview

class LinkForm(forms.Form):
    link = forms.URLField()