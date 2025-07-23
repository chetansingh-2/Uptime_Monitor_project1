from django.forms.utils import ErrorList
from django import forms
from .models import Website

class CustomErrorList(ErrorList):
    def __init__(self, errors=None, renderer=None):
        super().__init__(errors)
        self.renderer = renderer

    def as_ul(self):
        if not self.data:
            return ''  # No output if no errors
        # Wrap in a div to contain the margin and avoid affecting parent layout
        return '<div class="text-red-400 text-sm"><ul class="mt-2">' + ''.join(f'<li>{e}</li>' for e in self.data) + '</ul></div>'

class WebsiteForm(forms.ModelForm):


    class Meta:
        model = Website
        fields = ['name', 'url']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-4 bg-slate-700 border-2 border-sky-500 rounded-lg text-white text-lg focus:outline-none focus:border-sky-400 focus:ring focus:ring-sky-400/30',
                'placeholder': 'Enter website name'
            }),
            'url': forms.URLInput(attrs={
                'class': 'w-full p-4 bg-slate-700 border-2 border-sky-500 rounded-lg text-white text-lg focus:outline-none focus:border-sky-400 focus:ring focus:ring-sky-400/30',
                'placeholder': 'https://example.com'
            }),
        }
        error_messages = {
            'name': {'required': 'Please enter a website name'},
            'url': {'required': 'Please enter a website URL', 'invalid': 'Please enter a valid URL'}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_class = CustomErrorList


# from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# from django.forms.utils import ErrorList
class CustomErrorList(ErrorList):
    def __init__(self, errors=None, renderer=None, **kwargs):
        super().__init__(errors)
        self.renderer = renderer

    def as_ul(self):
        if not self.data:
            return ''
        return '<div class="text-red-400 text-sm"><ul class="mt-2">' + ''.join(f'<li>{e}</li>' for e in self.data) + '</ul></div>'

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_class = CustomErrorList
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': (
                    'w-full px-5 py-3 bg-slate-800 text-white text-lg '
                    'rounded-xl border-2 border-white '
                    'focus:outline-none focus:ring-2 focus:ring-sky-400 '
                    'placeholder-white'
                ),
                'placeholder': field.label,
                'autocomplete': 'off'
            })

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')


