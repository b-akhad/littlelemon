from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),

    path('book/', views.book, name="book"),
    path('api/book',views.BookListCreateApiView.as_view()),  # apiView

    path('menu/', views.menu, name="menu"),
    path("api/menu",views.MenuListApiView.as_view()), # apiView

    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),
    path("api/menu/<int:pk>", views.SingleMenuApiView.as_view()), # apiView


    path('reservations/', views.reservations, name="reservations"),
    path('bookings', views.bookings, name='bookings'),     
    path('login/',views.LoginView.as_view(),name='login'), # apiView
    path('refresh-token/',views.RefreshView.as_view(),name='refresh'), # apiView
    path('logout/',views.LogOutView.as_view(),name='logout'), # apiView
    path('whoami/',views.WhoAmIView.as_view(),name='whoami'), # apiView
    path('api-token-auth/', obtain_auth_token), # apiView

]

