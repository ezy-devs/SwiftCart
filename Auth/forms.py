from django.contrib.auth.models import User

from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm, PasswordChangeForm

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


