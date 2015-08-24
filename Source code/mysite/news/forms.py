from django import forms


class CountryCategoryForm(forms.Form):
    country = forms.ChoiceField()
    category = forms.ChoiceField()


class ArticlesForm(forms.Form):
    articles = forms.CheckboxInput()