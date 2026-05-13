from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('students.urls')),
    path('', include('courses.urls')),
    path('', include('registrations.urls')),
    path('', include('tuition.urls')),
    path('', include('reports.urls')),
    path('', login_required(TemplateView.as_view(template_name='index.html')), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=True)),
    path('accounts/logout/', RedirectView.as_view(url='/logout/', permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
