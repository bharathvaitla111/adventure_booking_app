from datetime import date

from allauth.account.views import email
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate
from .forms import LoginForm, RegistrationForm, Forgot, BookingForm
from .models import Booking, Customer, User
from django.views.generic import View
from django.shortcuts import render


# Create your views here.


class LoginSignup(View):
    def get(self, request):
        user_session = LoginForm()
        user_signup = RegistrationForm()
        context = {'form': user_session, 'signup': user_signup}
        return render(request, 'jumpstart/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        user_signup = RegistrationForm(request.POST)
        if form.is_valid() and 'first_name' not in request.POST.keys():
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is None:
                messages.error(request, "Incorrect username or password")
                return render(request, 'jumpstart/login.html', {'form': form})
            request.session['user_id'] = user.id
            return render(request, 'jumpstart/new_home.html', {'form': form, 'user': user})

        elif user_signup.is_valid():
            user_signup.save()
            form.email = user_signup.cleaned_data['email']
            return render(request, 'jumpstart/login.html', {'form': form})
        else:
            messages.error(request, "Please enter a Strong password")
            user_signup.first_name = user_signup.cleaned_data['first_name']
            user_signup.last_name = user_signup.cleaned_data['last_name']
            user_signup.email = user_signup.cleaned_data['email']
            context = {'form': LoginForm(), 'signup': user_signup}
            return render(request, 'jumpstart/login.html', context)


class Welcome(View):
    def get(self, request):
        return render(request, 'jumpstart/new_home.html')


class OrderHistoryView(View):
    template_name = 'jumpstart/order_history.html'

    def get(self, request):
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        customer = Customer.objects.get(id=user_id)
        bookings = Booking.objects.filter(customer=customer)
        context = {'bookings': bookings,
                   'user': user}

        # Add ticket count details to context if any of them are greater than zero
        for booking in bookings:
            if booking.adultTicketCount > 0 or booking.ChildTicketCount > 0 or \
                    booking.FastTrackAdultTicketCount > 0 or booking.FastTrackChildTicketCount > 0 or \
                    booking.SeniorCitizenTicketCount > 0 or booking.AdultCollegeIdOfferTicketCount > 0:
                context['has_ticket_details'] = True
                context['adult_tickets'] = booking.adultTicketCount
                context['child_tickets'] = booking.ChildTicketCount
                context['fast_track_adult_tickets'] = booking.FastTrackAdultTicketCount
                context['fast_track_child_tickets'] = booking.FastTrackChildTicketCount
                context['senior_citizen_tickets'] = booking.SeniorCitizenTicketCount
                context['college_id_offer_tickets'] = booking.AdultCollegeIdOfferTicketCount
                break

        return render(request, self.template_name, context)


class BookingSuccessView(View):
    template_name = 'jumpstart/bookingsuccessful.html'

    def get(self, request, booking_id):
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        print(user)
        print(user_id)
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return HttpResponse("Booking not found", status=404)

        context = {
            'user': user,
            'booking': booking,
            'adult_ticket_count': booking.adultTicketCount if booking.adultTicketCount > 0 else None,
            'child_ticket_count': booking.ChildTicketCount if booking.ChildTicketCount > 0 else None,
            'fast_track_adult_ticket_count': booking.FastTrackAdultTicketCount if booking.FastTrackAdultTicketCount > 0 else None,
            'fast_track_child_ticket_count': booking.FastTrackChildTicketCount if booking.FastTrackChildTicketCount > 0 else None,
            'senior_citizen_ticket_count': booking.SeniorCitizenTicketCount if booking.SeniorCitizenTicketCount > 0 else None,
            'adult_college_id_offer_ticket_count': booking.AdultCollegeIdOfferTicketCount if booking.AdultCollegeIdOfferTicketCount > 0 else None,
        }

        return render(request, self.template_name, context)


class ForgotPassword(View):

    def get(self, request):
        user_forgot = Forgot()
        reset = None
        context = {'form': user_forgot, 'reset': reset}
        return render(request, 'jumpstart/forgot_password.html', context)

    def post(self, request):
        form = Forgot(request.POST)
        reset = None
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'])
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return HttpResponseRedirect(reverse('login'))
        elif reset is None:
            user = authenticate(email=form.cleaned_data['email'])
            if user is None:
                messages.error(request, "Incorrect email")
                return render(request, 'jumpstart/forgot_password.html', {'form': form, 'reset': reset})
            else:
                reset = Forgot()
                reset.initial['email'] = form.cleaned_data['email']
                messages.success(request, "proceed to reset")
                return render(request, 'jumpstart/forgot_password.html', {'reset': reset})


class CreateBookingView(View):
    form_class = BookingForm
    template_name = 'jumpstart/bookingpage.html'

    # @login_required()
    def get(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        print(user)
        print(user_id)
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'user': user})

    # @login_required()
    def post(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        customer = Customer.objects.get(id=user_id)
        print(user)

        form = self.form_class(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = customer
            booking.bookingDate = date.today()

            # Calculate total price based on form data
            adult_ticket_count = form.cleaned_data['adultTicketCount']
            child_ticket_count = form.cleaned_data['ChildTicketCount']
            fast_track_adult_ticket_count = form.cleaned_data['FastTrackAdultTicketCount']
            fast_track_child_ticket_count = form.cleaned_data['FastTrackChildTicketCount']
            senior_citizen_ticket_count = form.cleaned_data['SeniorCitizenTicketCount']
            adult_college_id_offer_ticket_count = form.cleaned_data['AdultCollegeIdOfferTicketCount']

            adult_ticket_price = 50
            child_ticket_price = 30
            fast_track_adult_ticket_price = 80
            fast_track_child_ticket_price = 50
            senior_citizen_ticket_price = 40
            adult_college_id_offer_ticket_price = 40

            total_price = (adult_ticket_count * adult_ticket_price) + (child_ticket_count * child_ticket_price) + (
                    fast_track_adult_ticket_count * fast_track_adult_ticket_price) + (
                                  fast_track_child_ticket_count * fast_track_child_ticket_price) + (
                                  senior_citizen_ticket_count * senior_citizen_ticket_price) + (
                                  adult_college_id_offer_ticket_count * adult_college_id_offer_ticket_price)

            booking.totalPrice = total_price

            booking.save()
            # message = "booking successful"
            return redirect('booking_success', booking_id=booking.id)
            # return redirect('jumpstart/bookingpage.html', message, )
        return render(request, self.template_name, {'form': form})
