from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("listing/<str:listing_id>", views.listing, name="listing"),
    path("login", views.log_in, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.log_out, name="logout"),
    path("profile", views.profile, name="profile"),
    path('chat/', views.chat_view, name='chat_view'),
    path('individual_chat/<int:user_id>/', views.individual_chat_view, name='individual_chat_view'),
    path('send_message/', views.send_message, name='send_message'),

    #API routes
    path("follow", views.follow, name="follow")
]