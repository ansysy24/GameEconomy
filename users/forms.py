from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from users.models import Profile, AdvancedUser


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    initials = forms.CharField()
    subdomain = forms.CharField()
    
    class Meta:
        model = AdvancedUser
        fields = ['username', 'email', 'password1', 'password2', 'initials', 'subdomain']

    def clean_email(self):
        data = self.cleaned_data['email']
        # add email validation here:
        # domain = data.split('@')[1]
        # domain_list = ['gmail.com']
        # if domain not in domain_list:
        #     raise forms.ValidationError("Please enter an Email Address with a valid domain")
        return data

    def clean_subdomain(self):
        subdomain = self.cleaned_data['subdomain']
        subdomain_list = [p.subdomain for p in Profile.objects.all()]
        if subdomain in subdomain_list:
            raise forms.ValidationError("This Subdomain is already taken, please choose another subdomain")
        return subdomain

    def clean_initials(self):
        initials = self.cleaned_data['initials']
        initials_list = [p.initials for p in Profile.objects.all()]
        if initials in initials_list:
            raise forms.ValidationError("These Initials are already taken, please choose another initials")
        return initials

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(user=user, initials=self.cleaned_data['initials'],
                                   subdomain=self.cleaned_data['subdomain'])
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['initials']
