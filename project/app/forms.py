from django import forms
from .models import CustomUser, BlogPost, Comment, Tag,Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    name = forms.CharField(max_length=100, required=True, help_text='Required. Enter your full name.')

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Set username to email
        user.name = self.cleaned_data['name']
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'profile_picture', 'github_link', 'linkedin_link', 'short_bio')

# class BlogPostForm(forms.ModelForm):
#     class Meta:
#         model = BlogPost
#         fields = ('title', 'category', 'content')


class BlogPostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category']






class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)




class CustomUserEditForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'profile_picture', 'github_link', 'linkedin_link', 'short_bio')
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'multiple': False}),
        }



