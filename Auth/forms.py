from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm, PasswordChangeForm
from django import forms



INPUT_CLASSES = 'input'
class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'password')

        widgets = {
            'username': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            
            'password': forms.PasswordInput(attrs={
                'class': INPUT_CLASSES,
            }),
        }

class RegisterForm(UserCreationForm):
    email = forms.CharField(max_length=120)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'input'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
        self.fields['username'].help_text = ''
        self.fields['password1'].widget.attrs['class'] = 'input'
        self.fields['password1'].help_text = ''
        self.fields['password2'].widget.attrs['class'] = 'input'
        self.fields['password2'].help_text = ''

    

class PasswordResetForm(SetPasswordForm):
    
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, user, *args, **kwargs):
        super(PasswordResetForm, self).__init__(user, *args, **kwargs)
        self.fields['new_password1'].widget.attrs['class'] = 'input'
        self.fields['new_password1'].help_text =''
        self.fields['new_password2'].widget.attrs['class'] = 'input'
        self.fields['new_password2'].help_text = ''

class ForgetPasswordForm(PasswordChangeForm):
    
    class Meta:
        model = User
        fields = ['__all__']

    def __init__(self, user, *args, **kwargs):
        super(PasswordResetForm, self).__init__(user, *args, **kwargs)
        self.fields['new_password1'].widget.attrs['class'] = 'input'
        self.fields['new_password1'].help_text =''
        self.fields['new_password2'].widget.attrs['class'] = 'input'
        self.fields['new_password2'].help_text = ''


