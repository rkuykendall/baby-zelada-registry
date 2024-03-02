from django.urls import path
from . import views

urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("gift/", views.create_gift, name="create_gift"),
    path("export-items/", views.export_items_csv, name="export_items_csv"),
    path("export-gifts/", views.export_gifts_csv, name="export_gifts_csv"),
]
