from django.urls import path
from . import views

urlpatterns = [
    # GET → Fetch all career listings
    path('', views.get_all_careers, name='career-list'),

    # GET → Fetch a single career by its ID
    path('<int:pk>/', views.get_career_detail, name='career-detail'),

    # POST → Submit a job application
    path('<int:pk>/apply/', views.apply_for_career, name='career-apply'),
]
