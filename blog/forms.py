from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "text",)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)


class SignUpForm(forms.Form):

    username = forms.CharField(max_length=100)
    email_address = forms.EmailField()
    password_1 = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(widget=forms.PasswordInput)

    def clean_password_2(self):
        password_1 = self.cleaned_data["password_1"]
        password_2 = self.cleaned_data["password_2"]

        if password_1 != password_2:
            raise forms.ValidationError("Passwords do not match")
        return password_2
