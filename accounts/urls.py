from django.urls import path
from . import views


urlpatterns = [
    path('user/',views.user),
    path('user/<int:user_id>',views.UserDetail),
    path('user/change_password/', views.change_password),
    path('accounts/login/', views.login_page),
]