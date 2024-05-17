from django import forms
from .models import *

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