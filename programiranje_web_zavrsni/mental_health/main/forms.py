from django import forms
from .models import MoodEntry, Tag

class MoodEntryForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by("name"),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = MoodEntry
        fields = ["mood", "stress", "note", "tags"]