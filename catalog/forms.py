from django import forms

from catalog.models import Product, Category, Version, VersionCategory


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'is_current' or field_name == 'is_active':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProhibitedWordsMixin:
    def clean(self):
        cleaned_data = super().clean()
        name = self.cleaned_data['name'].lower()
        description = self.cleaned_data['description'].lower()

        prohibited_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                            'радар']

        for word in prohibited_words:
            if word in name.lower():
                raise forms.ValidationError('Плохое название')
            if word in description.lower():
                raise forms.ValidationError('Плохое описание')

        return cleaned_data


class ProductForm(StyleFormMixin, ProhibitedWordsMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'image', 'category')


class CategoryForm(StyleFormMixin, ProhibitedWordsMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class VersionCategoryForm(forms.ModelForm):
    class Meta:
        model = VersionCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
