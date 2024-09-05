from django import forms
from . import models

class RegisterationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Your Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Your Password'
    }))

    class Meta:
        model = models.Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter Your First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Your Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email Address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Your Phone Number'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
