from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),                  # Home page
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('donate/', views.donate, name='donate'),         # donor.html page
    path('donations/', views.donations_list, name='donations_list'), # food.html page
    path('logistics/', views.logistics_view, name='logistics'),
    path('safety/', views.safety_view, name='safety'),
    path('rewards/', views.rewards_view, name='rewards'),
    path('rewards/certificate/', views.generate_certificate, name='generate_certificate'),
    path('security/', views.security_view, name='security'),
    path('auth/', views.auth_view, name='auth'),
    path('uiux/', views.uiux_view, name='uiux'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('tracking/', views.tracking_view, name='tracking'),
    path('volunteer/', views.volunteer_view, name='volunteer'),
    path('support/', views.support_create, name='support'),
    path('support/tickets/', views.support_list, name='support_list'),
    path('api/my-donations/', views.api_my_donations, name='api_my_donations'),
    path('api/notifications/', views.api_notifications, name='api_notifications'),
]
