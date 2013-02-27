# coding: utf-8

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from beagent.models import User, Review

class UserCreationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)

    class Meta:

        model = User
        fields = ('email', 'type')

    def clean_password_repeat(self):

        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')

        if password and password_repeat and password != password_repeat:
            raise forms.ValidationError('Passwords do not match')

        return password_repeat

    def save(self, commit=True):

        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user

class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()
    new_password = forms.CharField(widget=forms.PasswordInput, required=False)
    new_password_repeat = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:

        model = User

    def clean_password(self):
        return self.initial['password']

    def clean_new_password_repeat(self):

        new_password = self.cleaned_data.get('new_password')
        new_password_repeat = self.cleaned_data.get('new_password_repeat')

        if new_password and new_password_repeat and new_password != new_password_repeat:
            raise forms.ValidationError('Passwords do not match')

        return new_password_repeat

    def save(self, commit=True):

        user = super(UserChangeForm, self).save(commit=False)

        if self.cleaned_data['new_password']:
            user.set_password(self.cleaned_data['new_password'])
            if commit:
                user.save()

        return user

class UserAdmin(UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'type', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        ('Info', {'fields': ('email', 'type',)}),
        ('Permissions', {'fields': ('is_staff',)}),
        ('Dates', {'fields': ('last_login',)}),
        ('Password', {'classes': ('wide',), 'fields': ('password', 'new_password', 'new_password_repeat')})
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'type', 'is_staff', 'password', 'password_repeat')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

class ReviewAdmin(admin.ModelAdmin):

    list_display = ('user', 'reviewer', 'added')
    search_fields = ('user', 'reviewer')
    ordering = ('added',)

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Review, ReviewAdmin)
