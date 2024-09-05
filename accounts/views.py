from django.shortcuts import render, redirect
from django.views.generic import View
from . import forms
from . import models
from django.http import HttpResponse
from django.contrib import messages

class RegisterClassBaseView(View):
    def get(self, request):
        form = forms.RegisterationForm()
        context = {
            "form": form
        }
        return render(request, 'account/register.html', context)

    def post(self, request):
        form = forms.RegisterationForm(request.POST)
        if form.is_valid():

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = email.split('@')[0]
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']

            # Creating the user
            user = models.Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password
            )
            user.phone_number = phone_number
            user.save()
            messages.success(request , "Registration Successful")
            return redirect('account_app:register')
        else :
        
            context = {
                "form": form
            }
            return render (request , 'account/register.html' , context)
