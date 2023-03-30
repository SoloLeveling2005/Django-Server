from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from mysite import settings
from web import views

urlpatterns = [
    # todo GET - return template, POST - auth user
    path("", views.auth, name="auth"),

    # todo GET - delete cookie
    path('log_out/', views.log_out, name="log_out"),

    # todo GET - return template all ads
    path("home", views.home, name="home"),

    # todo GET - return template user info
    path("user/<str:user_id>", views.user, name="user"),

    # todo GET - return template one ad for edit, POST - edit this ad
    path("ad_edit/<str:ad_id>", views.ad_edit, name="ad_edit"),

    # todo GET - return template one ad form for create, POST - create this ad
    path("ad_new", views.ad_new, name="ad_new"),

    # todo GET - return template one ad
    path("ad/<str:ad_id>", views.ad, name="ad"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)