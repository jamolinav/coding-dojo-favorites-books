from django.forms import ModelForm, PasswordInput, TextInput
from django import forms
from ...models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        #fields = '__all__'
        fields = ['title', 'desc']
        #exclude = ['uploaded_by_id', 'users_who_like']
        widgets = {
            'title' : TextInput(attrs={'placeholder': '<título>'}),
            # 'desc' : TextInput(attrs={'placeholder': '<descripción>'}),
        }
        labels = {
            'title'  : 'Título',
            'desc'  : 'Descripción',
        }

    def clean(self):
        cleaned_data = super(BookForm, self).clean()
        title = cleaned_data.get("title")
        desc = cleaned_data.get("desc")
        if (len(title) < 2 or len(desc) < 5):
            raise forms.ValidationError(
                "Título >= 2 y Descripción >= 5"
        )
