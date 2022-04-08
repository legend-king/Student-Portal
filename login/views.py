from django.contrib import messages
from django.shortcuts import redirect, render, HttpResponse
from faculty_app.views import login_details
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['student_portal']
admin_collection = db['admin_login']
student_collection = db['student_login']
faculty_collection = db['faculty_login']

# Create your views here.
def index(request):
    global login_data, login_id
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        admin = list(admin_collection.find({'email':email, 'password':password}))
        if len(admin)==1:
            return HttpResponse("Admin Successfully Logged in")
        else:
            messages.add_message(request, 50, "Wrong email or password")
        faculty = list(faculty_collection.find({'email':email, 'password':password}))
        if len(faculty)==1:
            login_details(1, faculty[0]['_id'])
            return redirect('/faculty/attendance')
    return render(request, 'login.html')