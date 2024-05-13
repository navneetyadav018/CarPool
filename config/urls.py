# urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from shop.views import contact_view, register, signin, signout, vehicles, order, Profile

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
      path("profile",Profile,name = "profile")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)