from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password

class EmailAuth(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            customer = User.objects.get(email=email)
            print(f'hey authing {password}, {customer.password}, {check_password(password, customer.password)}')
            if password is not None and not check_password(password, customer.password):
                return None
        except ObjectDoesNotExist as e:
            return None
        return customer
