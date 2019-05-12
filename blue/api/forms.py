from django import forms

from core.models import Register, Item, Statistics


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ("description", "note")


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ("description", "period", "amount", "note", "date", "register")


class StatisticsForm(forms.ModelForm):
    class Meta:
        model = Statistics
        fields = ("formula", "description", "note")
