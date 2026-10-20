from django import forms
from .models import Announcement, validate_image_size


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'description', 'price', 'phone', 'address']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        # Фото приходят списком в поле images, которого нет в модели,
        # поэтому проверяем каждое сами: что это картинка и что она не больше 5 МБ
        check_photo = forms.ImageField(validators=[validate_image_size]).clean
        for photo in self.files.getlist('images'):
            check_photo(photo)

        return cleaned_data
