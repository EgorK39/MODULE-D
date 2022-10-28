from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        # fields = '__all__'
        fields = [
            'author',
            'titel_name',
            'text',
            'ranking',
            'postCategory',
        ]

    def clean(self):
        cleaned_data = super().clean()
        titel_name = cleaned_data.get('titel_name')
        text = cleaned_data.get('text')
        if text == titel_name:
            raise ValidationError(
                "Содержание новости не должно быть идентично названию."
            )
        return cleaned_data
