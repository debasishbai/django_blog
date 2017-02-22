from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User
import re


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "text",)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)


class SignUpForm(forms.Form):

    username = forms.CharField(max_length=100, required=True)
    email_address = forms.CharField(max_length=50, required=True)
    password_1 = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data["username"]
        email_address = self.cleaned_data["email_address"]
        password_1 = self.cleaned_data["password_1"]
        password_2 = self.cleaned_data["password_2"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")

        if password_1 != password_2:
            raise forms.ValidationError("Passwords do not match.")

        if not re.match(r"[\w.]+@\w+\.\w+$", email_address):
            raise forms.ValidationError("Invalid email address!")

        return self.cleaned_data


class ContactUsForm(forms.Form):

    name = forms.CharField(max_length=50, required=True)
    email_address = forms.CharField(max_length=50, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean(self):
        name = self.cleaned_data["name"]
        email_address = self.cleaned_data["email_address"]
        message = self.cleaned_data["message"]

        if not re.match(r"[\w.]+@\w+\.\w+$", email_address):
            raise forms.ValidationError("Invalid email address!")

        return self.cleaned_data
