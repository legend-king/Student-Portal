from django.contrib import admin
from django.urls import path
from faculty_app import views

urlpatterns = [
    path("attendance",views.attendance, name='attendance'),
    path("attendance/<key>", views.attendance_update, name="attendance-add"),
    path("attendance/add/<key>",views.attendance_add_new, name='attendance-add-new'),
    path("attendance/update/<key>/<dh>", views.attendance_update_dh, 
    name='attendance-update-dh'),
    path("attendance/update/<key>/<dh>/<regno>",views.attendance_update_dh_regno,
    name="attendance-update-dh-regno"),

]
