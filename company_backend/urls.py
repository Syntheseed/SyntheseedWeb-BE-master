from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/blogs/', include('blogs.urls')),
    path('api/contact/', include('contact.urls')),
    path('api/careers/', include('Careers.urls')),
    path("ckeditor/", include("ckeditor_uploader.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
