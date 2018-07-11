from django import forms
from website.models import UploadedImage

class LoginForm(forms.Form):
    username = forms.EmailField(
        label='E-mail',
        min_length=5,
        max_length=50,
        widget = forms.EmailInput(
            attrs = {
                'placeholder': 'your-email@domain.com'
                }
            )
        )
    password = forms.CharField(
        label = 'Senha',
        min_length = 6,
        max_length = 30,
        widget = forms.PasswordInput(
            attrs = {
                'placeholder': '**********'
                }
            )
        )

class SearchForm(forms.Form):
    search = forms.CharField(
        min_length=1,
        max_length=100,
        widget = forms.TextInput(
            attrs = {
                'placeholder': 'Search Friends'
                }
            )
        )

class UploadedImageForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ('upload', 'date_taken')

class UploadStatusForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ('status',)

    def __init__(self, *args, **kwargs):
        super(UploadStatusForm, self).__init__(*args, **kwargs)
        self.fields['status'].choices = UploadedImage.STATUS_CHOICES
        self.fields['status'].widget.attrs.update({'class':'form-control'})
