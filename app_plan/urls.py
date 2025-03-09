from django.urls import path
from . import views

urlpatterns = [
    path('', views.grade_calculator, name='grade_calculator'),
    path("export-pdf/", views.export_pdf, name="export_pdf"),
]