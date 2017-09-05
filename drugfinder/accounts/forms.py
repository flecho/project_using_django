# -*- coding: utf-8 -*-
from django import forms
# password, date_of_birth, email

from django.core.validators import MinValueValidator, MaxValueValidator

'''
	To bind data to a form, pass the data as dictionary as the first parameter to your Form class constructor.
	
	ex) data = {'subject': 'hello', 'age': 7}
	f = Contactform(data)

'''

'''
	The primary task of a Form object is to validate data. With a bound Form instance, call the "is_valid()" method to run validation and return a boolean designating whether the data was valid:
'''


class SignUpForm(forms.Form):
	email = forms.EmailField(max_length=255) 
	password = forms.CharField(widget=forms.PasswordInput)
	date_of_birth = forms.CharField(max_length=10)
	sex = forms.CharField(max_length=1)


## Maybe this form needs to be updated.

class GenerateRandomUserForm(forms.Form):
	total = forms.IntegerField(
		validators=[
			MinValueValidator(50),
			MaxValueValidator(500)	
		]
	)

#This form expects a positive integer field between 50 and 500. It looks like this.
