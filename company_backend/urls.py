from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework.authtoken.views import obtain_auth_token
from blogs.admin_views import BlogAdminListCreateView, BlogAdminDetailView
from Careers.admin_views import CareerAdminListCreateView, CareerAdminDetailView
from contact.admin_views import ContactAdminListView


def health_check(request):
    return HttpResponse("OK", status=200)


urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path('api/blogs/', include('blogs.urls')),
    path('api/contact/', include('contact.urls')),
    path('api/careers/', include('Careers.urls')),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    # Admin API
    path('api/admin/token/', obtain_auth_token, name='admin-token'),
    path('api/admin/blogs/', BlogAdminListCreateView.as_view(), name='admin-blog-list'),
    path('api/admin/blogs/<int:pk>/', BlogAdminDetailView.as_view(), name='admin-blog-detail'),
    path('api/admin/careers/', CareerAdminListCreateView.as_view(), name='admin-career-list'),
    path('api/admin/careers/<int:pk>/', CareerAdminDetailView.as_view(), name='admin-career-detail'),
    path('api/admin/contacts/', ContactAdminListView.as_view(), name='admin-contact-list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
