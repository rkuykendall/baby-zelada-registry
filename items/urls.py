from django.urls import path
from . import views

urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("gift/", views.create_gift, name="create_gift"),
]
