from django import forms
from .models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'image' ,'bio','gender','age','email','number']



# forms.py


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput)
    

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['order', 'name', 'email', 'feedback_text', 'rating']
        widgets = {
            'feedback_text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),  # Rating out of 5 stars
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['order'].queryset = Order.objects.filter(user=user)
        self.fields['order'].empty_label = "Select Order"



class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(attrs={'placeholder': 'Email Address', 'class': 'form-control'}))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')

        if not User.objects.filter(email=email, username=username).exists():
            raise ValidationError("The provided email and username do not match any user.")

        return cleaned_data
    
    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generates a one-use only link for resetting password and sends to the user.
        """
        email = self.cleaned_data["email"]
        username = self.cleaned_data["username"]
        user = User.objects.get(email=email, username=username)
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain_override
            domain = domain_override
        user_email = email
        context = {
            'email': user_email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': 'https' if use_https else 'http',
            **(extra_email_context or {}),
        }
        subject = render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = render_to_string(email_template_name, context)
        send_mail(subject, body, from_email, [user_email], html_message=html_email_template_name)
    
