from django.urls import path
from . import views

urlpatterns = [
    path('', views.grade_calculator, name='grade_calculator'),
    path("export-pdf/", views.export_pdf, name="export_pdf"),
    path("max_gpa/", views.max_gpa_view, name="max_gpa"),

]