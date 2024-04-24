# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('flight-search/', views.flight_search),
    path('register/', views.register),
    path('search_order/', views.search_order),
    path('get_customers_info/', views.get_customers_info),
    path('insert_customer/', views.insert_customer),
    path('is_ticket/', views.is_ticket),
    path('insert_flight/', views.insert_flight),
    path('delete_flight/',views.delete_flight),
    path('update_flight/',views.update_flight),
    path('search_flight/',views.search_flight),
    path('get_all_travelname/',views.get_all_travelname),
    path('select_date_travelname/',views.select_date_travelname),
    path('update_is_ticket/',views.update_is_ticket),
    path('is_ticket_simple/', views.is_ticket_simple)
]
