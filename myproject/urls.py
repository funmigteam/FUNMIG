from django.contrib import admin


from django.urls import path, include


from django.contrib.auth import views as auth_views


from django.conf import settings


from django.conf.urls.static import static


from core import views as core_views


urlpatterns = [


    path('secret/', admin.site.urls),


    path('', core_views.site_root, name='home'),


    path('', include('core.urls')),


    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),


    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),


    path('chat/', include('chat.urls')),


]


if settings.DEBUG:


    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

