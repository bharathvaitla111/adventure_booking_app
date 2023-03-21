from datetime import date

from allauth.account.views import email
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate
from .forms import LoginForm, RegistrationForm, Forgot, BookingForm
from .models import Booking, Customer, User


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
        customer = Customer.objects.get(id=user_id)
        bookings = Booking.objects.filter(customer=customer)
        context = {'bookings': bookings}
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
            message = "booking successful"
            return render(request, 'jumpstart/bookingsuccessful.html')
            # return redirect('jumpstart/bookingpage.html', message, )
        return render(request, self.template_name, {'form': form})
