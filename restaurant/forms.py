from django.forms import ModelForm
from .models import Booking
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser



# Code added for loading form data on the Booking page
class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username",)