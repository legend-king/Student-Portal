from django.contrib import admin
from django.urls import path
from admin_app import views

urlpatterns = [
    # path("student_register", views.student_register, name='admin/student_register'),
    # path("faculty_register", views.faculty_register, name='admin/faculty_register'),
    # path("student_add_details", views.student_add_details, name='admin/student_add_details'),
    # path("students/<regno>", views.student_details, name='student_details')
    path("student_register", views.student_register),
    path("faculty_register", views.faculty_register),
    path("student_add_details", views.student_add_details),
    path("students/<regno>", views.student_details,name='student-detail'),
    path("students/<regno>/edit", views.student_edit,name='student-edit-form'),
    path("subjects", views.subjects),
    path("subjects/<dept>",views.sem, name='sem'),
    path("subjects/<dept>/<sem>", views.subject_details, name='subject-details'),
    path("subjects/<dept>/<sem>/edit", views.subject_edit, name='subject-edit'),
    path("subjects/<dept>/<sem>/update/<subcode>", views.subject_update, name="subject-update"),
    path("subjects/<dept>/<sem>/delete/<subcode>",views.subject_delete,name='subject-delete'),

    # path("subjects/edit/<dept>/<sem>",views.subject_edit,name="subject-edit"),
    # path("subjects/<dept>")
]
