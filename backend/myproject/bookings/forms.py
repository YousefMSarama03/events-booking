from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    number_of_seats = forms.IntegerField(
        min_value=1, 
        max_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '1 seat',
            'readonly': 'readonly'
        })
    )
    
    class Meta:
        model = Booking
        fields = ['number_of_seats']
        
    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)
        
    def clean_number_of_seats(self):
        number_of_seats = self.cleaned_data['number_of_seats']
        if self.event:
            if number_of_seats > self.event.seats:
                raise forms.ValidationError(
                    f"Only {self.event.seats} seats available for this event."
                )
        return number_of_seats
