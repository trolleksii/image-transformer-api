from django import forms


class UploadImgForm(forms.Form):
    file = forms.ImageField()
