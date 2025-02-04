
from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings
from app.views import send_email

urlpatterns = [
    path('', views.accueil),
    path('home/', views.index),
    path('carte/', views.carte),
    path('send_email/', send_email, name='send_email'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)