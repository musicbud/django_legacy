from django import forms

class SetMyProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    bio = forms.CharField(max_length=500, required=False)
    display_name = forms.CharField(max_length=100, required=False)
    location = forms.CharField(max_length=100, required=False)
    photo = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
