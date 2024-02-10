from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['name'].initial = self.instance.user.get_full_name()
            self.fields['email'].initial = self.instance.user.email
            
        elif self.instance and not self.instance.user:
            user = self.initial.get('user')
            if user and user.is_authenticated:
                self.fields['name'].initial = user.get_full_name()
                self.fields['email'].initial = user.email