from django.urls import path
from . import views
urlpatterns = [
    path('home/', views.home_view, name='home_view'),
    path('book_ticket/',views.book_ticket,name='book_ticket'),
    path('submit_booking/', views.submit_booking, name='submit_booking'), 
    path('', views.signup_view, name='signup'),
    path('delete_package/<int:package_id>/', views.delete_package, name='delete_package'),

    path('orders/delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('orders/', views.order_list, name='order_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('success/', views.success, name='success'),
    path('submit-package/', views.submit_package, name='submit_package'),
    path('trip_package/',views.trip_package,name='trip_package'),
]
