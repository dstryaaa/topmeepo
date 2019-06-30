from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from first import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<int:user_id>/', views.index),
    path('signup/', views.Signup.as_view()),
    path('feed/', views.feed),
    path('login/', views.Login.as_view()),
    path('logout/', views.Logout.as_view()),
    path('index/', views.kek),
    path('like/<int:post_id>/', views.like),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)