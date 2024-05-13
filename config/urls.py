# urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from shop.views import contact_view, register, signin, signout, vehicles, order, create_checkout_session, success_view, cancel_view
from shop.views import *
from shop.views import profile_view, profile_update_view, profile_edit_view,ChangePasswordView,faq_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('about', TemplateView.as_view(template_name='about.html'), name='about'),

    path('contact', contact_view, name='contact'),
    path("register", register, name="register"),
    path("signin", signin, name="signin"),
    path("signout",signout,name = "signout"),
    path("vehicles", vehicles, name= "vehicles"),
    path("bill",order,name = "bill"),
    # create-checkout-session
    path('create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path('success/', success_view, name='success'),
    path('cancel/', cancel_view, name='cancel'),
     path('profile', profile_view, name='profile'),
    path('profile/create', profile_update_view, name='profile_update'),
    path('profile/edit', profile_edit_view, name='profile_edit'),
    
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('faq',faq_page,name = 'faq'),

]
    


if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)