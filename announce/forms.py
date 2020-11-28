from django import forms
from .models import Comment, Image

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'image')


