from django.http import HttpResponse
from django.shortcuts import render
from .forms import BookingForm
from .models import Menu
from django.core import serializers
from .models import Booking
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from django.conf import settings
from django.contrib.auth import authenticate
from django.middleware import csrf
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer


# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def reservations(request):
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html',{"bookings":booking_json})

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

# Add your code here to create new views
def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 


@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        data = json.load(request)
        exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
            reservation_slot=data['reservation_slot']).exists()
        if exist==False:
            booking = Booking(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
    
    date = request.GET.get('date',datetime.today().date())

    bookings = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(booking_json, content_type='application/json')








# Create your views here.




def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh_token":str(refresh),
        "access_token":str(refresh.access_token),
    }

class LoginView(APIView):
    def post(self, request, format=None):
        data = request.data
        response = Response()
        username = data.get('username',None)
        password = data.get('password',None)
        user = authenticate(username=username,password=password)

        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(

                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=data["access_token"],
                    expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                
                )
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                    value=data['refresh_token'],
                    expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                )

                csrf.get_token(request)
                response.data = {"Success":"Login successfully "}
                return response
            else:
                return Response({"No active":'This account is not active!'},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid":"Invalid username or password!"},status=status.HTTP_404_NOT_FOUND)
        


class RefreshView(APIView):
    def get(self,request,format=None):
        refresh_token = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH']
            )
        if refresh_token is None:
            raise AuthenticationFailed(
                'Authentication credentials were not provided.'
                )
        token = RefreshToken(refresh_token)
        response = Response()
        response.data = {'message':'Successfully refreshed'}
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=str(token.access_token),
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']

        )
        return response
    

class WhoAmIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer = UserSerializer

    
    def get(self,format=None):
        serializer = UserSerializer(self.request.data)
        return Response(serializer.data)
    

class LogOutView(APIView):
    def get(self, format=None):
        response = Response()
        response.data = {'message': 'Logged out'}
        response.delete_cookie(
            settings.SIMPLE_JWT['AUTH_COOKIE'], path='/',samesite='None'
        )
        response.delete_cookie(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'], path='/', samesite='None'  
        )
        response.delete_cookie(
            'csrftoken',path='/',samesite='None'
        )
        return response
