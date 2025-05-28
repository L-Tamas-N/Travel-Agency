from django import forms
from .models import User
import re
from django.contrib.auth.forms import PasswordChangeForm

class UserRegistrationFrom(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'birth_date', 'phone']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists!")
        return email
    
class UserChangeProfileImage(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_image']

class UserUpdateProfileInfo(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'birth_date']
        
class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
