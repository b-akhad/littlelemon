from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('reservations/', views.reservations, name="reservations"),
    path('menu/', views.menu, name="menu"),
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),  
    path('bookings', views.bookings, name='bookings'), 
    
    path('login/',views.LoginView.as_view(),name='login'),
    path('refresh-token/',views.RefreshView.as_view(),name='refresh'),
    path('logout/',views.LogOutView.as_view(),name='logout'),
    path('whoami/',views.WhoAmIView.as_view(),name='whoami'),
    path('api-token-auth/', obtain_auth_token),

]

