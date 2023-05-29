from django.urls import path
from . import views

urlpatterns = [path('login/', views.login_user, name='login'),
               path('logout/', views.logout_user, name='logout'),
               path('register/', views.register_user, name='register'),
               path('account/', views.user_account, name='account'),
               path('edit-account/', views.edit_account, name='edit-account'),
               path('create-certificate/', views.create_certificate, name='create-certificate'),
               path('edit-certificate/<str:pk>/', views.edit_certificate, name='edit-certificate'),
               path('delete-certificate/<str:pk>/', views.delete_certificate, name='delete-certificate'),
               path('', views.profiles, name='profiles'),
               path('profile/<str:pk>/', views.user_profile, name='user-profile'),
               path('inbox/', views.inbox, name='inbox'),
               path('message/<str:pk>/', views.view_message, name='message'),
               path('send-message/<str:pk>/', views.create_message, name='send-message'),
               ]
