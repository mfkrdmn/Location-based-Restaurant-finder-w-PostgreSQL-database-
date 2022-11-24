from django import forms
from .models import User

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput()) # bu sekilde confirm password olayini da ekliyoruz

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    
    def clean(self): #raise error if passwords doesnt match
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )