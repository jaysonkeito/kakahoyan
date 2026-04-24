from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    discussion_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    discussion_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
    event_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Appointment
        fields = [
            'client_name', 'client_email', 'client_phone',
            'event_type', 'event_date', 'expected_guests', 'notes',
            'discussion_type', 'discussion_date', 'discussion_time', 'client_address',
        ]
        widgets = {
            'client_name':     forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
            'client_email':    forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'client_phone':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': '09XX XXX XXXX'}),
            'event_type':      forms.Select(attrs={'class': 'form-select'}),
            'expected_guests': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 80'}),
            'notes':           forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any additional details or questions...'}),
            'discussion_type': forms.Select(attrs={'class': 'form-select', 'id': 'id_discussion_type'}),
            'client_address':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Brgy. XX, Bayawan City'}),
        }