from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import TerapeutaUser


class TerapeutaUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def save(self, terapeuta=None, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            if terapeuta:
                TerapeutaUser.objects.create(usuario=user, terapeuta=terapeuta)
        
        return user