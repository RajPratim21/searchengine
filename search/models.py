# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms 
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from django.db import models

# Create your models here.
	


class Ex1Widget(forms.MultiWidget):
    _choices = (('this', 'This'),('this', 'This'))
    def __init__(self, choices, attrs=[]):
        self._choices = choices
        super(Ex1Widget, self).__init__(attrs)


    def render(self, name, value, attrs=None):
        output = []

        for k, v in self._choices:
            output.append('<div><input type="button" style="font-size: auto; vertical-align: top;background-color: #008CBA; border-radius: 18px; float:left;" class="btn" value="%s" /></div>' % v)

        return self.format_output(output)
class RegistrationForm(forms.Form):
	username = forms.CharField(label='Username', max_length=30)
	email = forms.EmailField(label='Email')
	password1 = forms.CharField(label='Password',widget=forms.PasswordInput())
	password2 = forms.CharField(label='Retype',widget=forms.PasswordInput())
	
        choices = forms.MultipleChoiceField(label="Keywords:",widget=forms.CheckboxSelectMultiple(attrs={'class':'checkbox-inline'}),choices=(('this', 'This'), ('that', 'That'), ('other', 'Other Thing that is good very good'),('another','wow wonderfull'),('very','very much awesome'),('great','great staff'),('peculier','peculier staff')))
	
	def clean_username(self):
		print "Called clean username"
		username = self.cleaned_data['username']
		if not re.search(r'^\w+$', username):
			raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
		try:
			User.objects.get(username=username)
		except ObjectDoesNotExist:
			return username
		except MultipleObjectsReturned:
			raise forms.ValidationError('Username is already taken.')
		raise forms.ValidationError('Username is already taken.')

	def clean_password2(self):
		if 'password1' in self.cleaned_data:
			password1 = self.cleaned_data['password1']
			password2 = self.cleaned_data['password2']
		if password1 == password2:
			return password2
		raise forms.ValidationError('Passwords do not match.')
class KeywordsForm(forms.Form):
	choices = forms.MultipleChoiceField(label="choose your keywords",widget=Ex1Widget(choices=(('this', 'This'), ('that', 'That'), ('other', 'Other Thing'))))

