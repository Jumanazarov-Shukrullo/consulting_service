from django import forms
from taggit.forms import TagWidget

from .models import Post

GEEKS_CHOICES = (
    ("1", "One"),
    ("2", "Two"),
    ("3", "Three"),
    ("4", "Four"),
    ("5", "Five"),
)


class EmailForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class SearchForm(forms.Form):
    query = forms.CharField()


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    services = forms.ChoiceField(choices=GEEKS_CHOICES)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=13, required=True)
    message = forms.Textarea()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'tags', 'body', 'status', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tags': TagWidget(attrs={'data-role': 'tags input', 'placeholder': 'Add Tags', 'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            # 'status': forms.ChoiceField(required=True)
        }
