from django import forms as forms

class UserForm(forms.Form):
	# Contact info
	first_name = forms.CharField(label="First Name", max_length=50)
	last_name = forms.CharField(label="Last Name", max_length=50)
	email = forms.EmailField(label="Email")
	phone_number = forms.CharField(label="Phone Number", max_length=11)

	# Login info
	username = forms.CharField(label="Username", max_length=50)
	password = forms.CharField(label="Password", widget=forms.PasswordInput(), max_length=100)

	# Payment info
	creditcard = forms.CharField(max_length=17)

	# Address info
	street = forms.CharField(max_length=100)
	city = forms.CharField(max_length=50)
	country = forms.CharField(max_length=50)
	zipcode = forms.CharField(max_length=9)
