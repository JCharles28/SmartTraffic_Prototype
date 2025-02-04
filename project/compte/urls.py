from django.urls import include, path
from django.contrib.auth import views as auth_views 
from django.conf import settings
from django.conf.urls.static import static
from compte import views



urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', views.deconnexion, name='logout'),
    path('connexion/', views.connexion),
    path('contact/', views.contact),
    # chemin vers la page de profil
    path('profil/', views.profil),
]
