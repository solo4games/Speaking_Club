from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from django.urls import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static

from apps.speaking_clubs.views import login


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    # path('robokassa/', include('robokassa.urls')),
    path('speaking_club/', include('speaking_clubs.urls')),
    path('login/', login, name='login'),
    path('', RedirectView.as_view(url=reverse_lazy('main_gc'))),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
