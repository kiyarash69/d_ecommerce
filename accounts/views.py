from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View

from cart.models import Cart, CartItem
from cart.views import _cart_id
from . import forms
from . import models
from django.contrib import messages
from .models import Account
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
import requests


# -
# region register , login and logout

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

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string(
                'account/account_verification_email.html',
                {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                }
            )
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, "Registration Successful")
            return redirect(reverse('account_app:login') + '?command=verification&email=' + email)
        else:
            context = {
                "form": form
            }
            return render(request, 'account/register.html', context)


# -
class LoginClassBaseView(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()

                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Getting the product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # Get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id_list = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id_list.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id_list[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except Cart.DoesNotExist:
                pass

            login(request, user)
            messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)
            except:
                return redirect('account_app:dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('account_app:login')

        return render(request, 'accounts/login.html')

    def get(self, request):
        return render(request, 'account/login.html')


# -
@login_required(login_url='account_app:login')
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('account_app:login')


# endregion


# region dashboard etc .

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        login(request, user)
        return redirect('home')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('account_app:register')


class DashboardClassBaseView(LoginRequiredMixin, View):
    login_url = 'account_app:login'

    def get(self, request):
        return render(request, 'account/dashboard.html', {})


class ForgotPasswordClassBaseView(View):
    def get(self, request):
        # Pass an empty dictionary as context (best practice)
        return render(request, 'account/forgot_password.html', {})

    def post(self, request):
        email = request.POST.get('email')  # Corrected typo

        # Use filter to avoid exceptions
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)  # Get the user after verifying email exists

            # Change Password Verification
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string(
                'account/reset_password_message.html',
                {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                }
            )
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('account_app:login')
        else:
            messages.error(request, 'Email does not exist!')
            return redirect('account_app:forgot_p')


class ResetPasswordValidate(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            request.session['uid'] = uid
            messages.success(request, 'Please reset your password')
            return redirect('account_app:reset_password')
        else:
            messages.error(request, 'This link has been expired!')
            return redirect('account_app:login')


class ResetPassword(View):
    def get(self, request):
        return render(request, 'account/reset_password.html')

    def post(self, request):
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            uid = request.session.get('uid')

            if uid:  # Check if uid exists in the session
                try:
                    user = Account.objects.get(pk=uid)
                    user.set_password(password)
                    user.save()
                    messages.success(request, 'Password reset successful')
                    return redirect('account_app:login')
                except Account.DoesNotExist:
                    messages.error(request, 'User does not exist!')
                    return redirect('account_app:reset_password')
            else:
                messages.error(request, 'Session expired, try again.')
                return redirect('account_app:reset_password')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('account_app:reset_password')

# endregion
