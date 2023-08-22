from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={"class": "form-control", "placeholder": "Mensagem"}
        ),
        label="",              
    )

    class Meta:
        model = Message
        exclude = ('user',)