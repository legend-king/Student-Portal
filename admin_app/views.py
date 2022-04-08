from django.shortcuts import render, HttpResponse
from django.http import HttpResponseNotFound, QueryDict
import pymongo
from django.contrib import messages
from admin_app import my_classes
from login.views import login_details

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['student_portal']
student_collection = db['student_login']
faculty_collection = db['faculty_login']
subject_list={'robo':"Robotics and Automation",'cse':"Computer Science and Engineering"
,'csbs':"Computer Science and Business System",'csd':"Computer Science and Design",
'aero':"Aeronautical Engineering",'auto':"Automobile Engineering",
'aiml':"Artificial Intelligence and Machine Learning",'mecha':"Mechatronics",
'mech':"Mechanical Engineering",'it':"Information Technology",'ft':"Food Technology",
'chem':"Chemical Engineering", 'ece':"Electronics and Communication Engineering",
'eee':"Electrical and Electronics Engineering",'civil':"Civil Engineering",
'biotechnology':"Biotechnology",'biomedical':"Biomedical Engineering"}
subject_collection = db['subjects']
attendance_collection = db['attendance']

# Create your views here.
def student_register(request):
    # if login_info[0]==-1:
    #     return HttpResponseNotFound("Go and login first")
    if request.method=='POST':
        name = request.POST.get('name')
        rollno = request.POST.get('rollno')
        email = request.POST.get('email')
        password = request.POST.get('password')
        student_collection.insert_one({'name':name,'_id':rollno,'email':email,
        'password':password})
        messages.success(request, 'Student added successfully')
    return render(request, 'admin/student_register.html')

def faculty_register(request):
    # if login_info[0]==-1:
    #     return HttpResponseNotFound("Go and login first")
    if request.method=='POST':
        name = request.POST.get('name')
        staffcode = request.POST.get('staffcode')
        email = request.POST.get('email')
        password = request.POST.get('password')
        faculty_collection.insert_one({'name':name,'_id':staffcode,'email':email,
        'password':password})
        messages.success(request, 'Faculty added successfully')
    return render(request, 'admin/faculty_register.html')


def student_add_details(request):
    # if login_info[0]==-1:
    #     return HttpResponseNotFound("Go and login first")
    students = list(student_collection.find({}, {'_id':1}))
    student = [x['_id'] for x in students]
    context={'data':student}
    return render(request, 'admin/student_list.html', context)

def student_details(request, regno):
    # if login_info[0]==-1:
    #     return HttpResponseNotFound("Go and login first")
    # if request.method=="POST":
    #     department = request.POST.get('department')
    #     section = request.POST.get('section')
    #     year = request.POST.get('year')
    #     print(department, section, year)
    #     # student_collection.update_one({'_id':regno}, {'department':department})
    x=list(student_collection.find({'_id':regno}))
    if 'department' not in x[0]:
        y=my_classes.Student(x[0]['name'],x[0]['_id'], x[0]['email'])
    else:
        y=my_classes.Student(x[0]['name'],x[0]['_id'],x[0]['email'],
        subject_list[x[0]['department']]
        ,x[0]['year'],x[0]['section'],x[0]['semester'])
    context = {'student':y}
    if len(x)==0:
        return HttpResponseNotFound("<h1>No such register number exists !</h1>")
    if request.method=="GET":
        return render(request,'admin/student.html',context)
    elif request.method=="PUT":
        data = QueryDict(request.body).dict()
        student_collection.update_one({'_id':regno},{'$set':{'name':data['name'],
        'year':data['year'],'department':data['department'],'section':data['section'],
        'semester':data['semester']}})
        y=my_classes.Student(x[0]['name'],x[0]['_id'],x[0]['email'],
        subject_list[data['department']]
        ,data['year'],data['section'],data['semester'])
    context = {'student':y}
    return render(request, 'admin/student.html', context)

def subjects(request):
    # if login_info[0]==-1:
    #     return HttpResponseNotFound("Go and login first")
    return render(request, "admin/subjects.html")

def sem(request, dept):
    # if login_info[0]==-1:
    #     return HttpResponseNotFound("Go and login first")
    if dept not in subject_list:
        return HttpResponseNotFound("<h1> No such department </h1>")
    y=list(subject_collection.find({'dept':dept}))
    if len(y)==0:
        subject_collection.insert_one({'dept':dept,'sem1':[],'sem2':[],'sem3':[],
        'sem4':[],'sem5':[],'sem6':[],'sem7':[],'sem8':[]})
    return render(request, "admin/sem.html", {'dept':dept})


def subject_details(request, dept, sem):
    # if login_info[0]==-1:
    #     return HttpResponseNotFound("Go and login first")
    if dept not in subject_list:
        return HttpResponseNotFound("<h1> No such department </h1>")
    if not sem.isdigit():
        return HttpResponseNotFound("<h1> not a correct sem number </h1>")
    if int(sem)<=0 or int(sem)>8:
        return HttpResponseNotFound("<h1> Sem value should be between 1 and 8</h1>")
    y=list(subject_collection.find({'dept':dept}))
    current_sem = "sem"+str(sem)
    s=[]
    tp=y[0][current_sem]
    for i in tp:
        s.append(my_classes.Subject(i[0],i[1]))
    context={'data':s, 'dept1':subject_list[dept],'dept':dept, 'sem':sem}
    if request.method=="GET":
        return render(request,'admin/subject.html',context)
    if request.method=="POST" and "edit" in request.POST:
        data1 = QueryDict(request.body).dict()
        for i in tp:
            if i[0]==data1['sub_code']:
                return HttpResponseNotFound("<h1> Sub code already exists </h1>")
        tp.append([data1['sub_code'], data1['sub_name']])
        current_sem = "sem"+str(sem)
        subject_collection.update_many({'dept':dept},
         {'$set':{current_sem:tp}})
    if request.method=="POST" and "update" in request.POST:
        data1 = QueryDict(request.body).dict()
        if data1['old_sub_code']!=data1['sub_code']:
            for i in tp:
                if i[0]==data1['sub_code']:
                    return HttpResponseNotFound("<h1> Sub code already exists </h1>")
        temp = [data1['sub_code'], data1['sub_name']]
        for i in range(len(tp)):
            if tp[i][0]==data1['old_sub_code']:
                tp[i]=temp
        current_sem = "sem"+str(sem)
        subject_collection.update_many({'dept':dept},
        {'$set':{current_sem:tp}})
    s=[]
    for i in tp:
        s.append(my_classes.Subject(i[0],i[1]))
    context={'data':s, 'dept1':subject_list[dept],'dept':dept, 'sem':sem}
    return render(request, "admin/subject.html", context)
    

# def subject_department(request, dept):
#     if dept not in subject_list:
#         return HttpResponseNotFound("<h1>No such department !</h1>")
#     y=list(subject_collection.find({'dept':dept}))
#     if len(y)==0:
#         subject_collection.insert_one({'dept':dept,'sem1':[],'sem2':[],'sem3':[],
#         'sem4':[],'sem5':[],'sem6':[],'sem7':[],'sem8':[]})
#     s=[]
#     for i in [['CS19441','OS'],['CS19442','SE'],['CS19443','DBMS']]:
#         s.append(my_classes.Subject(i[0],i[1]))
#     context={'data':[my_classes.Subject_Detail(1,s),
#     my_classes.Subject_Detail(2,'sem2'),my_classes.Subject_Detail(3,'sem3'),
#     my_classes.Subject_Detail(4,'sem4'),my_classes.Subject_Detail(5,'sem5'),
#     my_classes.Subject_Detail(6,'sem6'),my_classes.Subject_Detail(7,'sem7'),
#     my_classes.Subject_Detail(8,'sem8')], 'dept':dept}
#     if request.method=="GET":
#         return render(request,'subject.html',context)
#     if request.method=="PUT":
#         print("Sem : ",current_sem)
#         data1 = QueryDict(request.body).dict()
#         print(data1)
#     return render(request, "subject.html",context)


def student_edit(request,regno):
    # if login_info[0]==-1:
    #     return HttpResponseNotFound("Go and login first")
    x=list(student_collection.find({'_id':regno}))
    if len(x)==0:
        return HttpResponseNotFound("<h1>No such register number exists !</h1>")
    if 'department' not in x[0]:
        y=my_classes.Student(x[0]['name'],x[0]['_id'], x[0]['email'])
    else:
        y=my_classes.Student(x[0]['name'],x[0]['_id'],x[0]['email'],x[0]['department']
        ,x[0]['year'],x[0]['section'],x[0]['semester'])
    context = {'student':y}
    return render(request,"partials/student_edit_form.html",context)


def subject_edit(request, dept, sem):
    # if login_info[0]==-1:
    #     return HttpResponseNotFound("Go and login first")
    if dept not in subject_list:
        return HttpResponseNotFound("<h1> No such department exists</h1>")
    if not sem.isdigit():
        return HttpResponseNotFound("<h1> not a correct sem number </h1>")
    if int(sem)<=0 or int(sem)>8:
        return HttpResponseNotFound("<h1> Sem value should be between 1 and 8</h1>")
    # print(dept, sem)
    context={'dept':dept, 'sem':sem}
    return render(request, "partials/subject_edit_form.html", context)

def subject_update(request, dept, sem, subcode):
    # if login_info[0]==-1:
    #     return HttpResponseNotFound("Go and login first")
    if dept not in subject_list:
        return HttpResponseNotFound("<h1> No such department exists</h1>")
    if not sem.isdigit():
        return HttpResponseNotFound("<h1> not a correct sem number </h1>")
    if int(sem)<=0 or int(sem)>8:
        return HttpResponseNotFound("<h1> Sem value should be between 1 and 8</h1>")
    y = subject_collection.find_one({'dept':dept})
    current_sem="sem"+str(sem)
    tp = y[current_sem]
    tp1=[]
    tp2=None
    for i in tp:
        if i[0]==subcode:
            tp1=i
            tp2=my_classes.Subject(i[0],i[1])
    if tp1==[]:
        return HttpResponseNotFound("<h1>No Such subject code exists</h1>")
    context = {'dept':dept, 'data':tp2, 'sem':sem}
    return render(request, "admin/subject_update.html", context)

# def subject_delete(request, dept, sem, subcode):
#     if dept not in subject_list:
#         return HttpResponseNotFound("<h1> No such department exists</h1>")
#     if not sem.isdigit():
#         return HttpResponseNotFound("<h1> not a correct sem number </h1>")
#     if int(sem)<=0 or int(sem)>8:
#         return HttpResponseNotFound("<h1> Sem value should be between 1 and 8</h1>")
#     # print(dept, sem)
#     context={'dept':dept, 'sem':sem}
#     return render(request, "partials/subject_edit_form.html", context)

def subject_delete(request, dept, sem, subcode):
    # if login_info[0]==-1:
    #     return HttpResponseNotFound("Go and login first")
    if dept not in subject_list:
        return HttpResponseNotFound("<h1> No such department exists</h1>")
    if not sem.isdigit():
        return HttpResponseNotFound("<h1> not a correct sem number </h1>")
    if int(sem)<=0 or int(sem)>8:
        return HttpResponseNotFound("<h1> Sem value should be between 1 and 8</h1>")
    y = subject_collection.find_one({'dept':dept})
    current_sem="sem"+str(sem)
    tp = y[current_sem]
    tp1=[]
    for i in range(len(tp)):
        if tp[i][0]==subcode:
            tp1=i
            tp.pop(i)
            break
    subject_collection.update_one({'dept':dept}, {'$set':{current_sem:tp}})
    if tp1==[]:
        return HttpResponseNotFound("<h1>No Such subject code exists</h1>")
    s=[]
    for i in tp:
        s.append(my_classes.Subject(i[0],i[1]))
    context={'dept':dept,'sem':sem,'data':s, 'dept1':subject_list[dept]}
    return render(request, "admin/subject.html", context)


def attendance(request):
    # if login_info[0]==-1:
    #     return HttpResponseNotFound("Go and login first")
    x=list(attendance_collection.find())
    data=[]
    for i in x:
        data.append(my_classes.Attendance(i['dept'],i['sem'],i['year'],i['sub_code']
        ,"",i['staff_code'],i['section']))
    if request.method=="POST" and "edit" in request.POST:
        data1 = QueryDict(request.body).dict()
        del data1['edit']
        del data1['csrfmiddlewaretoken']
        temp = list(attendance_collection.find(data1))
        if len(temp)>0:
            return HttpResponseNotFound("Already exists")
        else:
            temp1=""
            for i in data1.values():
                temp1+=str(i)
            data1['key']=temp1
            attendance_collection.insert_one(data1)
        data.append(my_classes.Attendance(data1['dept'],data1['sem'],data1['year'],
        data1['sub_code'], "", data1['staff_code'],data1['section']))
    context={'data':data}
    return render(request, 'admin/attendance.html', context)


def attendance_add(request):
    # if login_info[0]==-1:
    #     return HttpResponseNotFound("Go and login first")
    return render(request, "partials/attendance_edit_form.html")