from django.http import HttpResponse, HttpResponseNotFound, QueryDict
from django.shortcuts import render
from faculty_app.models import Attendance, AttendanceDetail, AttendanceDH
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['student_portal']
attendance_collection = db['attendance']
attendance_details_collection = db['attendance-details']
student_collection = db['student_login']
login_data=-1
login_id=None
# Create your views here.
def attendance(request):
    if login_data!=1:
        return HttpResponseNotFound("<h1> Go and Login first idiot</h1>")
    a = list(attendance_collection.find({'staff_code':login_id}))
    if len(a)==0:
        return HttpResponse("<h1> No class allocated to you till now </h1>")
    data1=[]
    for i in a:
        data1.append(Attendance(i['staff_code'],i['key'],i['dept'],
        i['section'],i['year'],i['sem'],i['sub_code']))
    context = {'data':data1}
    return render(request, 'faculty/attendance.html', context)


def attendance_update(request, key):
    temp = list(attendance_details_collection.find({'key':key}))
    data=[]
    for i in temp:
        data.append(AttendanceDetail(i['date'],i['hour'],i['date']+i['hour']))
    if request.method=="POST" and "edit" in request.POST:
        data1=QueryDict(request.body).dict()
        temp=list(attendance_details_collection.find({'key':key, 
        'date':data1['date'], 'hour':data1['hour']}))
        if len(temp)>0:
            return HttpResponse("Already Exists")
        temp=attendance_collection.find_one({'key':key}, {'dept':1
        ,'section':1, 'sem':1,'year':1})
        
        temp1=student_collection.find({'department':temp['dept'], 
        'section':temp['section'], 'year':temp['year'],
         'semester':temp['sem']}, {'_id':1})

        attendance_data={}
        for i in temp1:
            attendance_data[i['_id']]=1

        attendance_details_collection.insert_one({'key':key, 'date':data1['date'], 
        'hour':data1['hour'], 'attendance':attendance_data})
        data.append(AttendanceDetail(data1['date'],data1['hour'],
         data1['date']+data1['hour']))
    context={'data':data, 'key':key}
    return render(request, "faculty/attendance_add.html", context)

def attendance_add_new(request, key):
    context = {'key':key}
    return render(request, "faculty/attendance_add_new.html", context)


def attendance_update_dh(request, key, dh):
    temp=list(attendance_details_collection.find({'key':key,'date':dh[:-1],'hour':dh[-1]},
    {'attendance':1}))
    data=temp[0]['attendance']
    data1=[]
    for i in data:
        data1.append(AttendanceDH(i, data[i]))
    context={'data':data1, 'key':key, 'dh':dh}
    return render(request, 'faculty/attendance_update_dh.html', context)

def attendance_update_dh_regno(request, key, dh, regno):
    temp=list(attendance_details_collection.find({'key':key,'date':dh[:-1],'hour':dh[-1]},
    {'attendance':1}))
    data=temp[0]['attendance']
    if data[regno]==0:
        data[regno]=1
    else:
        data[regno]=0
    attendance_details_collection.update_one({'key':key, 'date':dh[:-1], 'hour':dh[-1]},
    {'$set':{'attendance':data}})
    data1=[]
    for i in data:
        data1.append(AttendanceDH(i, data[i]))
    context={'key':key, 'dh':dh, 'data':data1}
    return render(request, 'faculty/attendance_update_dh.html', context)


def login_details(a, b):
    global login_data, login_id
    login_data=a
    login_id=b
