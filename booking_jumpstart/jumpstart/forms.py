from django.forms import ModelForm, TextInput, EmailInput, PasswordInput, forms
from .models import Customer, Booking
from django import forms
from django.contrib.auth.hashers import make_password

from django.contrib.auth.forms import UserCreationForm


class LoginForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['email', 'password']
        widgets = {
            # telling Django your password field in the mode is a password input on the template
            'email': EmailInput(attrs={
                'placeholder': 'enter a valid email',
            }),
            'password': PasswordInput(attrs={
                'placeholder': 'enter your password',
                'required': True
            })
        }


class RegistrationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            # telling Django your password field in the mode is a password input on the template
            'first_name': TextInput(attrs={
                'placeholder': 'enter your firstname',
            }),
            'last_name': TextInput(attrs={
                'placeholder': 'enter your lastname',
            }),
            'email': EmailInput(attrs={
                'placeholder': 'enter your email',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(
            attrs={'placeholder': 'enter your password'})
        self.fields['password2'].widget = PasswordInput(
            attrs={'placeholder': 're-enter your password'})

        for fieldname in ['first_name', 'last_name', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def save(self, commit=True):
        username = self.cleaned_data['first_name'] + '_' + self.cleaned_data['last_name']
        new_customer = Customer(
            username=username,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=make_password(self.cleaned_data['password1'])
        )
        new_customer.save()


class Forgot(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['email', 'password1', 'password2']
        widgets = {
            # telling Django your password field in the mode is a password input on the template
            'email': EmailInput(attrs={
                'placeholder': 'enter a valid email',
            })
        }

    def __init__(self, *args, **kwargs):
        super(Forgot, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(
            attrs={'placeholder': 'enter your password'})
        self.fields['password2'].widget = PasswordInput(
            attrs={'placeholder': 're-enter your password'})

        # self.fields['email'].help_text = None

    def clean(self):
        pass


class BookingForm(ModelForm):
    adultTicketPrice = 50
    ChildTicketPrice = 30
    FastTrackAdultTicketPrice = 80
    FastTrackChildTicketPrice = 50
    SeniorCitizenTicketPrice = 40
    AdultCollegeIdOfferTicketPrice = 40

    class Meta:
        model = Booking
        fields = [

            'reserveDate',
            'address',
            'phoneNumber',
            'adultTicketCount',
            'ChildTicketCount',
            'FastTrackAdultTicketCount',
            'FastTrackChildTicketCount',
            'SeniorCitizenTicketCount',
            'AdultCollegeIdOfferTicketCount',
            # 'totalPrice',
        ]
        widgets = {
            'reserveDate': forms.DateInput(attrs={'type': 'date'}),
            'adultTicketCount': forms.NumberInput(attrs={'class': 'ticket-count-input'}),
            'ChildTicketCount': forms.NumberInput(attrs={'class': 'ticket-count-input'}),
            'FastTrackAdultTicketCount': forms.NumberInput(attrs={'class': 'ticket-count-input'}),
            'FastTrackChildTicketCount': forms.NumberInput(attrs={'class': 'ticket-count-input'}),
            'SeniorCitizenTicketCount': forms.NumberInput(attrs={'class': 'ticket-count-input'}),
            'AdultCollegeIdOfferTicketCount': forms.NumberInput(attrs={'class': 'ticket-count-input'}),
        }

    def clean(self):
        adultTicketPrice = 50
        ChildTicketPrice = 30
        FastTrackAdultTicketPrice = 80
        FastTrackChildTicketPrice = 50
        SeniorCitizenTicketPrice = 40
        AdultCollegeIdOfferTicketPrice = 40

        cleaned_data = super().clean()

        adult_ticket_count = cleaned_data.get('adultTicketCount', 0)
        child_ticket_count = cleaned_data.get('ChildTicketCount', 0)
        fast_track_adult_ticket_count = cleaned_data.get('FastTrackAdultTicketCount', 0)
        fast_track_child_ticket_count = cleaned_data.get('FastTrackChildTicketCount', 0)
        senior_citizen_ticket_count = cleaned_data.get('ChildTicketCount', 0)
        adult_college_id_offer_ticket_count = cleaned_data.get('AdultCollegeIdOfferTicketCount', 0)

        cleaned_data['totalPrice'] = (adult_ticket_count * adultTicketPrice) + (
                    child_ticket_count * ChildTicketPrice) + (fast_track_adult_ticket_count * FastTrackAdultTicketPrice) + (fast_track_child_ticket_count * FastTrackChildTicketPrice)+ (senior_citizen_ticket_count * SeniorCitizenTicketPrice) + (adult_college_id_offer_ticket_count * AdultCollegeIdOfferTicketPrice)
        return cleaned_data
