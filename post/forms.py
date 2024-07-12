from django import forms
from .models import Post

class NewPostForm(forms.ModelForm):
    tags = forms.CharField(max_length=255, required=False)
    class Meta:
        model = Post
        fields = ['picture', 'caption', 'tags']
