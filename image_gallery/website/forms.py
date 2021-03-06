from django import forms
from website.models import UploadedImage, User, UserData

# ----------------------------------------- LOGIN -----------------------------------------------
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
        label = 'Password',
        min_length = 6,
        max_length = 30,
        widget = forms.PasswordInput(
            attrs = {
                'placeholder': '**********'
                }
            )
        )


# -------------------------------------- GALLERY ORDERING -----------------------------------------
class GalleryOrderingForm(forms.Form):
    DATE_TAKEN = 'date_taken'
    NUMBER_OF_LIKES = 'likes'

    ASCENDING = 'asc'
    DESCENDING = 'desc'

    SORTING_CHOICES = (
        (DATE_TAKEN, 'Date Taken'),
        (NUMBER_OF_LIKES, 'Number of Likes'),
    )

    ORDERING_CHOICES = (
        (ASCENDING, 'Ascending'),
        (DESCENDING, 'Descending'),
    )

    sort_by = forms.ChoiceField(choices=SORTING_CHOICES, widget=forms.widgets.Select(attrs={'class':'form-control'}))
    order = forms.ChoiceField(choices=ORDERING_CHOICES, widget=forms.widgets.Select(attrs={'class':'form-control'}))


# ---------------------------------------- REQUEST ACCESS -----------------------------------------
class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your-email@domain.com'}),
            'password': forms.PasswordInput(attrs={'placeholder': '**********'}),
        }


# ---------------------------------------- USER'S PROFILE -----------------------------------------
class UpdateUserForm(UserForm):
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields.pop('password', None)

class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ('profile_picture',)

# ------------------------------------------ SEARCH ----------------------------------------------
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
