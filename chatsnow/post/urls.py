from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.post_list, name = "post_list"),
    path("create/", views.post_create, name = "post_create"),
    path("<int:post_id>/edit", views.post_update, name = "post_update"),
    path("<int:post_id>/deleted", views.post_delete, name = "post_delete"),
    path("register/",views.register_user, name = "register"),
    path("search/", views.search_users, name = "search"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)