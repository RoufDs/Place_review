from django.urls import path, include

from .views import home, place_details, user_login, log_user_out, writer_page, place_edit


urlpatterns = [
    path('', home, name='home'),
    path('writer/<int:pk>/', writer_page, name='writer'),
    path('login/', user_login, name='user_login'),
    path('logout/', log_user_out, name='log_user_out'),
    path('place_details/<int:pk>/', place_details, name='place_details'),
    path('place_edit/<int:pk>/', place_edit, name='place_edit')
]
