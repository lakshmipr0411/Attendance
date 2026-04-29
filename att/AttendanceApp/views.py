from django.shortcuts import render
from django.http import HttpResponseRedirect
import sys
from datetime import datetime,date
import time
print (sys.executable)
import mysql.connector
db = mysql.connector.connect(host="localhost",user="root",password="",database="members",port = "3306")
c=db.cursor()
# Create your views here.
def index (request):
    msg = " "
    if request.POST:
        Name = request.POST.get("name")
        Mobile = request.POST.get("mob")
        Gender = request.POST.get("gender")
        Email = request.POST.get("email")
        Location = request.POST.get("Location")
        print (Name)
        s = " Select count(*) From log where Mobile_Number='" + Mobile + "'"
        c.execute(s)
        col = c.fetchone()
        if col[0]:
            msg = "Alearedy Registerd"
        else: 
           s= "insert into member_details (Member_Name,Mobile_Number,Gender,Email,Location) values ('"+ Name +"','"+ Mobile +"','"+ Gender +"','"+ Email +"','"+ Location +"')"
           try: 
               c.execute(s)
               db.commit()
           except:
               msg = "error"
           else:
               msg = "Added Success Fullly"
           s= "insert into log (Member_Name,Mobile_Number,Roll) values ('"+ Name +"','"+ Mobile +"' , 'user')"
           try:
                c.execute(s)
                db.commit()
           except:
               msg = "error"
           else:
               msg = "Added Success Fullly"
    return render (request,"index.html",{"msg":msg})
def login (request):
    msg = " "
    name = request.POST.get('name')
    mobile = request.POST.get('mob')
    s = "select count(*) from log where Mobile_Number ='" + str(mobile) + "'"
    c.execute(s)
    i = c.fetchone()
    if i[0] > 0:
        s = "select * from log where Mobile_Number ='" + str(mobile) + "'"
        c.execute(s)
        i = c.fetchone()
        if i[1] == name:
            request.session["mobile"] = mobile
            if i[2] == "admin":
                return HttpResponseRedirect("/admin")
            if i[2] == "user":
                return HttpResponseRedirect("/userform")
        else:
            msg = "You are not authorized to login"
    else:
            msg = "User doesnot Exist"
    return render(request,"login.html",{"msg": msg})
def userform(request):
    mobile = request.session.get("mobile")
    s = "select * from member_details where Mobile_Number= '" + mobile + "'"
    c.execute(s)
    i = c.fetchall()
    t = "select * from attendance where Mobile_Number= '" + mobile + "'"
    c.execute(t)
    x = c.fetchall()
    return render(request,"userform.html", {"i": i, "x": x})
def registerattendance(request):
    msg = " "
    mobile = request.session.get("mobile")
    mid = request.GET.get("mid")
    atime = datetime.now().strftime("%H:%M:%S")
    adate = date.today()
    s = "select meetdate  from meeting where meetdate= '" + str(adate) + "'"
    c.execute(s)
    x = c.fetchone()
    mdate = x[0]
    if mdate > adate:
        msg = "Meeting is not today"
        return render(request, "userform.html", {"msg": msg})
    elif mdate == adate:
        s = "select * from member_details where Mobile_Number= '" + str(mobile) + "'"
        c.execute(s)
        i = c.fetchone()
        mname = i[1]
        print(atime)
        print(mname)
        # ✅ Check if attendance already marked today
        check = "SELECT * from attendance where Mobile_Number='" + mobile + "' and Attendancedate='" + str(adate) + "'"
        c.execute(check)
        result = c.fetchall()
        if result:
            msg = "Attendance already marked today"
            return render(request,"userform.html",{"msg": msg})
            #return HttpResponseRedirect("/userform")
        else:
            s = "insert into attendance(Member_Name,Mobile_Number,Member_ID,Attendancedate,Attendancetime) values('" + str(
                mname) + "','" + str(
                mobile) + "',(select Member_ID from member_details where Mobile_number='" + mobile + "'),'" + str(
                adate) + "','" + str(atime) + "')"
            try:
                c.execute(s)
                db.commit()
            except:
                msg = "error"

            else:
                msg = "Added Success Fullly"
                print(msg)
                return render (request, "userform.html", {"msg": msg})
                #return HttpResponseRedirect("/userviewattendance")
    else:
        msg = "meeting is not today"
        return render(request, "userform.html", {"msg": msg})
def admin (request):
    s = "select * from member_details"
    c.execute(s)
    i = c.fetchall()
    return render(request, "admin.html", {"i": i})
def adminviewattendance(request):
    mid = request.GET.get("mid")
    s = "select * from member_details where Member_ID='" + str(mid) + "'"
    c.execute(s)
    y = c.fetchall()
    s = "select * from attendance where Member_ID='" + str(mid) + "' order by Attendancedate DESC"
    c.execute(s)
    i = c.fetchall()
    return render(request,"adminviewattendance.html",{"i": i,"y":y})
def searchbydate(request):
    sdate = request.POST.get("sdate") # use GET
    if not sdate: 
       return render(request,"searchbydate.html",{"i":[],"error": "Please select a date"})
    s="SELECT *FROM attendance Where Attendancedate = %s"
    c.execute(s, (sdate,)) # safe Query
    i = c.fetchall()
    return render(request, "searchbydate.html",{"i":i})
def addmeetdate(request):
    msg = ""
    if request.POST:
        mdate = request.POST.get("mdate")

        # 🔍 Check count
        s = "SELECT COUNT(*) FROM meeting WHERE meetdate=%s"
        c.execute(s, (mdate,))
        i = c.fetchone()

        print(i)

        if i[0] == 0:
            # ✅ Insert only if not exists
            s = "INSERT INTO meeting(meetdate) VALUES (%s)"
            try:
                c.execute(s, (mdate,))
                db.commit()
                msg = "Added Successfully ✅"
            except:
                msg = "Error while inserting ❌"
        else:
            # ❌ Already exists
            msg = "Meeting date already exists ❗"
            print (msg)
    return render(request, "addmeetdate.html", {"msg": msg})