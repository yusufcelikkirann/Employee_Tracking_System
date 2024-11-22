from django import forms
from .models import CustomUser

class EmployeeForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}),
        label="Password",
        help_text="Leave blank to keep the current password.",
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'annual_leave', 'role', 'password']

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Şifreyi hashleyerek kaydet
        if self.cleaned_data['password']:
            instance.set_password(self.cleaned_data['password'])
        if commit:
            instance.save()
        return instance
