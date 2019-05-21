from django import forms

from core.models import Register, RegisterRow, Statistics, StatisticsRowRegister, StatisticsRowStatistics


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ("description", "note")


class RegisterRowForm(forms.ModelForm):
    class Meta:
        model = RegisterRow
        fields = ("description", "period", "amount", "note", "date", "register")


class StatisticsForm(forms.ModelForm):
    class Meta:
        model = Statistics
        fields = ("description", "note")


class StatisticsRowRegisterForm(forms.ModelForm):
    class Meta:
        model = StatisticsRowRegister
        fields = ("parent_statistics", "register")


class StatisticsRowStatisticsForm(forms.ModelForm):
    class Meta:
        model = StatisticsRowStatistics
        fields = ("parent_statistics", "statistics")
