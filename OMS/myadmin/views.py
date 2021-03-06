from django.db import connection
from django.shortcuts import render,redirect
from django.http import HttpResponse
from helpers.format import format_query
from helpers.format import executeSQL
from helpers.navbar import which_nav
from helpers.email import send_email, extract_emails
from helpers.idgenerator import randomStr
import datetime

# Create your views here.
def admin(request):
    utype = request.session.get('usertype')
    logged_in = request.session.get('logged_in')
    print(logged_in)
    if logged_in:
        navname = "logged_navbar.html"
    else:
        navname = "navbar.html"
        
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": navname})

    return render(request, 'myadmin/admin_home.html', {"nav": navname})

def orphans_list(request):
    logged_in = request.session.get('logged_in')
    utype = request.session.get('usertype')

    if logged_in:
        navname = "logged_navbar.html"
    else:
        navname = "navbar.html"
    
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": navname})

    sql = f"SELECT * FROM Orphan"
    orphans = executeSQL(sql, ['CNIC', 'Name', 'DateOfBirth', 'Education', 'Sex', 'Special Needs'])

    return render(request, 'myadmin/orphans_list.html', {"orphans":orphans, "titles": list(orphans[0].keys()), "nav": navname}) # This will pass the orphans as a js object
    # Please prettify the html. 
    # # beauty lies in the heart.

def employees_list(request):
    logged_in = request.session.get('logged_in')
    utype = request.session.get('usertype')

    if logged_in:
        navname = "logged_navbar.html"
    else:
        navname = "navbar.html"
    
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": navname})

    sql = fr"SELECT * FROM Employees"
    employees = executeSQL(sql, ['CNIC', 'DeptID', 'Name', 'DateOfBirth', 'JoinDate', 'ContractEndDate', 'Email', 'Phone', 'Salary'])

    return render(request, 'myadmin/employees_list.html', {"employees":employees, "titles": list(employees[0].keys()), "nav": navname}) # This will pass the orphans as a js object 

def volunteers_list(request):
    logged_in = request.session.get('logged_in')
    utype = request.session.get('usertype')

    if logged_in:
        navname = "logged_navbar.html"
    else:
        navname = "navbar.html"
    
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": navname})

    sql = fr"SELECT Volunteers.CNIC, DeptID, Name, Age, Sex, JoinDate, ContractEndDate, Phone, Organization, Status, Email FROM Volunteers inner join Users where Volunteers.CNIC = Users.CNIC"
    volunteers = executeSQL(sql, ['CNIC', 'DeptID', 'Name', 'Age', 'Sex', 'JoinDate', 'ContractEndDate', 'Phone', 'Organization', 'Status', 'Email'])
    # for x in volunteers:
    #     x['Email'] = executeSQL(fr"select Email from Users where CNIC='{x['CNIC']}'", ['Email'])[0]['Email']

    return render(request, 'myadmin/volunteers_list.html', {"volunteers":volunteers, "titles": list(volunteers[0].keys()), "nav": navname}) 

def view_list(request):
    logged_in = request.session.get('logged_in')
    utype = request.session.get('usertype')

    if logged_in:
        navname = "logged_navbar.html"
    else:
        navname = "navbar.html"
    
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": navname})

    return render(request, 'myadmin/view_list.html', {"nav": navname}) 

def add_orphan(request):
    logged_in = request.session.get('logged_in')
    utype = request.session.get('usertype')

    if logged_in:
        navname = "logged_navbar.html"
    else:
        navname = "navbar.html"
    
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": navname})
    
    return render(request, 'myadmin/add_orphan.html', {"nav": navname})

def add_orphan_record(request):
    logged_in = request.session.get('logged_in')
    utype = request.session.get('usertype')

    if request.method == "POST" and logged_in and utype == 'admin':
        CNIC = request.POST["CNIC"]
        Name = request.POST["name"]
        SpecialNeeds = request.POST["specialneeds"]
        DateOfBirth=request.POST["DateOfBirth"]
        Education=request.POST["education"]
        Sex=request.POST["sex"]
        Hobbies=request.POST["hobbies"]
        sql = fr"INSERT INTO Orphan (CNIC, Name, SpecialNeeds, DateOfBirth, Education, Sex) VALUES('{CNIC}', '{Name}', '{SpecialNeeds}','{DateOfBirth}', '{Education}', '{Sex}');"
        print([x for x in request.POST.items()])
        try:
            executeSQL(sql)
        except:
            return render(request, 'myadmin/cnic_exists.html', {"nav": which_nav(request)})
    
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": which_nav(request)})
    
    return redirect('myadmin:orphans_list')
    
def update_orphan(request, orphanid):

    orphid = orphanid.split('=')[1]

    sql = fr"select * from Orphan where CNIC='{orphid}'"
    result = executeSQL(sql, ['CNIC', 'Name', 'DateOfBirth', 'Education', 'Sex', 'SpecialNeeds'], True)

    print("updating this orphan:", result)

    logged_in = request.session.get('logged_in')
    utype = request.session.get('usertype')
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": which_nav(request)})

    return render(request, 'myadmin/update_orphan.html', {"result":result[0],"titles": list(result[0].keys()), "nav": which_nav(request)})
    
def update_record_o(request):
    logged_in = request.session.get('logged_in')
    utype = request.session.get('usertype')
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": which_nav(request)})
    # sql("update Orphan where CNIC=id")
    if request.method == "POST":
        CNIC = request.POST["CNIC"]
        Name = request.POST["name"]
        SpecialNeeds = request.POST["specialneeds"]
        DateOfBirth=request.POST["DateOfBirth"]
        Education=request.POST["education"]
        Sex=request.POST["sex"]
        
        print([(x,k) for x,k in request.POST.items()])

        sql = fr"Update Orphan set Name='{Name}', SpecialNeeds='{SpecialNeeds}', DateOfBirth='{DateOfBirth}', Education='{Education}', Sex='{Sex}' where CNIC='{CNIC}';"
        executeSQL(sql)
    
    return redirect('/myadmin/view/orphanslist/')

def update_volunteer(request, volunteerid):

    volid = volunteerid.split('=')[1]

    sql = fr"select * from Volunteers where CNIC='{volid}'"
    result = executeSQL(sql, ['CNIC', 'DeptID', 'Name', 'Age', 'Sex', 'JoinDate', 'ContractEndDate', 'Phone', 'Organization', 'Status'])
    
    print("updating this volunteer:", result)
    
    logged_in = request.session.get('logged_in')
    utype = request.session.get('usertype')
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": which_nav(request)})

    status = result[0]['Status']
    if status == 'Pending':
        deptid = result[0]['DeptID']
        sql = fr"SELECT DeptName FROM Department WHERE DeptID = '{deptid}'"
        department = executeSQL(sql, ['department'])[0]['department']
        return render(request, 'myadmin/approve_volunteer.html', {'result':result[0], 'Department':department, 'nav': which_nav(request)})

    email = executeSQL(fr"select Email from Users where CNIC='{volid}'", ['Email'])

    result2 = executeSQL(sql, ['CNIC', 'DeptID', 'Name', 'Age', 'Sex', 'JoinDate', 'ContractEndDate', 'Phone', 'Organization', 'Status'], True)
    result2[0]['Email'] = email[0]['Email']    
    return render(request, 'myadmin/update_volunteer.html', {"result":result2[0],"titles": list(result[0].keys()), "nav": which_nav(request)})

def approve_volunteer(request):
    logged_in = request.session.get('logged_in')
    utype = request.session.get('usertype')
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": which_nav(request)})

    cnic = request.POST['cnic']
    if request.method == 'POST':
        status = request.POST['status']
        sql = fr"select Email from Users where CNIC='{cnic}' and Usertype='Volunteer'"
        email = executeSQL(sql, ['Email'])[0]['Email']
        sql = fr"Update Volunteers set Status='{status}' where CNIC='{cnic}';"
        message = f"Hello\n\n Your Application status with this orphanage is {status}\n\nBest Regards,\nOMS"
        send_email([email], message, "Volunteer Application Status")
        executeSQL(sql)
    return redirect('myadmin:volunteers_list')
    

def update_record_v(request):
    logged_in = request.session.get('logged_in')
    utype = request.session.get('usertype')
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": which_nav(request)})
    # sql("update Orphan where CNIC=id")
    if request.method == "POST":
        CNIC = request.POST["CNIC"]
        Name = request.POST["name"]
        join = request.POST["JoinDate"]
        end=request.POST["EndDate"]
        Sex=request.POST["sex"]
        email=request.POST["email"]
        dept=request.POST["deptid"]
        org=request.POST["organization"]
        phone=request.POST["phone"]
        age=request.POST["age"]
        
        print([(x,k) for x,k in request.POST.items()])
    # ['CNIC', 'DeptID', 'Name', 'Age', 'Sex', 'JoinDate', 'ContractEndDate', 'Phone','Email',  'Organization']
        sql = fr"Update Volunteers set Name='{Name}', DeptID='{dept}', Age='{age}', JoinDate='{join}', Sex='{Sex}', ContractEndDate='{end}', Organization='{org}', Phone='{phone}' where CNIC='{CNIC}';"
        executeSQL(sql)

        executeSQL(fr"Update Users set Email='{email}' where CNIC='{CNIC}'")
    
    return redirect('/myadmin/view/volunteerslist/')

def update_employee(request, employeeid):

    eid = employeeid.split('=')[1]

    sql = fr"select * from Employees where CNIC='{eid}'"
    result = executeSQL(sql, ['CNIC', 'DeptID', 'Name', 'DateOfBirth',  'JoinDate', 'ContractEndDate', 'Email','Phone', 'Salary'], True)
    
    print("updating this employee:", result)
    
    logged_in = request.session.get('logged_in')
    utype = request.session.get('usertype')
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": which_nav(request)})
    
    return render(request, 'myadmin/update_employee.html', {"result":result[0],"titles": list(result[0].keys()), "nav": which_nav(request)})

def update_record_e(request):
    logged_in = request.session.get('logged_in')
    utype = request.session.get('usertype')
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": which_nav(request)})
    # sql("update Orphan where CNIC=id")
    if request.method == "POST":
        CNIC = request.POST["CNIC"]
        Name = request.POST["name"]
        join = request.POST["JoinDate"]
        end=request.POST["EndDate"]
        email=request.POST["email"]
        dept=request.POST["deptid"]
        prevdept=request.POST["prevdeptid"]
        salary=request.POST["salary"]
        phone=request.POST["phone"]
        dob=request.POST["dateofbirth"]
        
        print([(x,k) for x,k in request.POST.items()])
    # ['CNIC', 'DeptID', 'Name', 'Age', 'Sex', 'JoinDate', 'ContractEndDate', 'Phone','Email',  'Organization']
        sql = fr"Update Employees set Name='{Name}', DeptID='{dept}', DateOfBirth='{dob}', JoinDate='{join}', ContractEndDate='{end}', Email='{email}', Salary='{salary}', Phone='{phone}' where CNIC='{CNIC}';"
        executeSQL(sql)
        
        sql = fr"SELECT NumberOfEmployees FROM Department WHERE DeptID='{dept}'"
        total = int(executeSQL(sql, ['numberofemployees'])[0]['numberofemployees'])
        total = total + 1
        strdept = str(dept)
        sql = f"UPDATE Department SET NumberOfEmployees = {total} WHERE DeptID='{strdept}'"
        executeSQL(sql)

        sql = fr"SELECT NumberOfEmployees FROM Department WHERE DeptID='{prevdept}'"
        total = int(executeSQL(sql, ['numberofemployees'])[0]['numberofemployees'])
        total = total - 1
        strdept = str(prevdept)
        sql = f"UPDATE Department SET NumberOfEmployees = {total} WHERE DeptID='{strdept}'"
        executeSQL(sql)

    return redirect('/myadmin/view/employeeslist/')

def adoption_request_list(request):
    logged_in = request.session.get('logged_in')
    utype = request.session.get('usertype')
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": which_nav(request)})

    sql = fr"SELECT * FROM AdoptionRequest"
    result = executeSQL(sql, ['ApplicationID', 'OrphanCNIC', 'ParentCNIC', 'Status'])
    return render(request, 'myadmin/adoption_request_list.html', {"requests":result,"titles": list(result[0].keys()), "nav": which_nav(request)})

def update_request_view(request, applicationid):
    logged_in = request.session.get('logged_in')
    utype = request.session.get('usertype')
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": which_nav(request)})
    sql = fr"SELECT * FROM AdoptionRequest WHERE ApplicationID='{applicationid}'"
    result = executeSQL(sql, ['ApplicationID', 'OrphanCNIC', 'ParentCNIC', 'Status'])
    return render(request, 'myadmin/adoption_request.html', {"result":result[0],"titles": list(result[0].keys()), "nav": which_nav(request)})

    
def update_request(request):
    utype = request.session.get('usertype')
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": which_nav(request)})
    if request.method == 'POST':
        status = request.POST['status']
        appid = request.POST['applicationid']
        sql = fr"UPDATE AdoptionRequest SET Status='{status}' WHERE ApplicationID='{appid}'"
        executeSQL(sql)
        sql = fr"select Email from AdoptionRequest inner join Users on AdoptionRequest.ParentCNIC=Users.CNIC where ApplicationID={appid}"
        address = executeSQL(sql, ['Email'])
        if status=="Approved":
            message= "We are pleased to inform you that your adoption application #" + appid + " has been accepted!"
            subject= "Congratulations!"
        elif status=="Denied":
            message= "We are sorry to say that your adoption application #" + appid + " has been rejected."
            subject= "Apologies"
        else:
            print("Email error")
            return redirect('myadmin:adoption-request-list')
        print(address)
        send_email([address[0]['Email']], message, subject)

    return redirect('myadmin:adoption-request-list')

def mass_email(request):
    utype = request.session.get('usertype')
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": which_nav(request)})
    if request.method == 'POST':
        content = request.POST['email-content']
        subject = request.POST['email-subject']
        sql = fr"SELECT Email FROM Users limit 10"
        addresses = executeSQL(sql, ['Email'])
        addresses = extract_emails(addresses)
        send_email(addresses, content, subject)
        return redirect('/myadmin/')
    return render(request, 'myadmin/mass_email.html',{"nav": which_nav(request)})
        

def appointment_list(request):
    logged_in = request.session.get('logged_in')
    utype = request.session.get('usertype')
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": which_nav(request)})

    sql = fr"SELECT * FROM Appointment"
    result = executeSQL(sql, ['AppointmentID', 'ParentCNIC', 'AdminCNIC', 'AppointmentTime', 'Status'])
    return render(request, 'myadmin/appointment_list.html', {"requests":result,"titles": list(result[0].keys()), "nav": which_nav(request)})

def update_appointment_view(request, appointmentid):
    logged_in = request.session.get('logged_in')
    utype = request.session.get('usertype')
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": which_nav(request)})

    sql = fr"SELECT * FROM Appointment WHERE AppointmentID='{appointmentid}'"
    result = executeSQL(sql, ['AppointmentID', 'ParentCNIC', 'AdminCNIC', 'AppointmentTime', 'Status'])
    return render(request, 'myadmin/appointment_edit.html', {"result":result[0],"titles": list(result[0].keys()), "nav": which_nav(request)})

def update_appointment(request):
    utype = request.session.get('usertype')
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": which_nav(request)})
    if request.method == 'POST':
        status = request.POST['status']
        appid = request.POST['appointmentid']

        sql = fr"UPDATE Appointment SET Status='{status}' WHERE AppointmentID='{appid}'"
        executeSQL(sql)
        sql = fr"select Email from Appointment inner join Users on Appointment.ParentCNIC=Users.CNIC where AppointmentID='{appid}'"
        address = executeSQL(sql, ['Email'])
        print('emails found', address)
        if status=="Approved":
            message= "We are pleased to inform you that your appointment slot with id " + appid + " has been scheduled!"
            subject= "Congratulations!"
        elif status=="Denied":
            message= "We are sorry to say that your appointment #" + appid + "could not be schedule. Kindly make another appointment request."
            subject= "Apologies"
        else:
            print("Email error")
            return redirect('myadmin:adoption-request-list')
        
        send_email([address[0]['Email']], message, subject)

    return redirect('myadmin:appointmentspage')

def add_transaction(request):
    departments = executeSQL("select DeptID, DeptName from Department", ["id", "name"])
    print(departments)
    return render(request, "myadmin/add_transaction.html", {"dept": departments,"nav": which_nav(request)} )


def add_trans_don(request):
    logged_in = request.session.get('logged_in')
    utype = request.session.get('usertype')

    if request.method == "POST" and logged_in and utype == 'admin':
        transID = request.POST["transactionid"]
        Amount = request.POST["amount"]
        Donor = request.POST["donor"]
        DateOfDonation=request.POST["donationdate"]
        X=-1
        Y=None
        sql = fr"INSERT INTO Transactions (ID, Amount, DeptID, Donor, DateOfExpense, DateOfDonation) VALUES('{transID}', '{Amount}','{X}', '{Donor}','{Y}','{DateOfDonation}');"
        print([x for x in request.POST.items()])
        try:
            executeSQL(sql)
        except:
            return render(request, 'myadmin/transid_exists.html', {"nav": which_nav(request)})
    
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": which_nav(request)})
    
    return redirect('/myadmin/add_transaction.html/', {"nav": which_nav(request)})

def add_trans_exp(request):
    logged_in = request.session.get('logged_in')
    utype = request.session.get('usertype')
    if request.method == "POST" and logged_in and utype == 'admin':
        transID = randomStr()
        Amount = request.POST["amount"]
        Amount1=int(Amount)*-1
        DeptID = request.POST["deptid"]
        Date=request.POST["expensedate"]
        sql = fr"INSERT INTO Expenses (ID, Amount, DeptID, Date) VALUES('{transID}', {Amount1}, '{DeptID}','{Date}');"
        print(sql)
        print([x for x in request.POST.items()])
        try:
            executeSQL(sql)
        except Exception as E:
            print(E)
            return render(request, 'myadmin/transid_exists.html', {"nav": which_nav(request)})
    
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": which_nav(request)})
    
    return redirect('/myadmin/addtransaction/', {"nav": which_nav(request)})



def view_transaction(request):
    sql = fr"SELECT ID AS ID, Amount, Date FROM Expenses union select TransactionID AS ID, Amount, Date from Donation order by Date;"
    result = executeSQL(sql, ['ID','Amount' ,'Date'])
    sql2 = fr"select SUM(Amount) from Expenses"
    sql3 = fr"select SUM(Amount) from Donation"
    balancee=executeSQL(sql2,['Balance'])
    balances=executeSQL(sql3,['Balance'])
    total= int(balancee[0]['Balance'])+int(balances[0]['Balance'])
    print("viewing this volunteer:", result)
    
    logged_in = request.session.get('logged_in')
    utype = request.session.get('usertype')
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": which_nav(request)})
    return render(request, 'myadmin/view_transaction.html', {"result":result,"titles": list(result[0].keys()),"balance":total , "nav": which_nav(request)})

def add_employee(request):
    utype = request.session.get('usertype')
    if utype != 'admin':
        return render(request, 'myadmin/not_admin.html', {"nav": which_nav(request)})
    if request.method == 'POST':
        CNIC = request.POST["CNIC"]
        Name = request.POST["name"]
        join = request.POST["JoinDate"]
        end=request.POST["EndDate"]
        email=request.POST["email"]
        dept=request.POST["deptid"]
        salary=request.POST["salary"]
        phone=request.POST["phone"]
        dob=request.POST["dateofbirth"]
        
        
        sql = fr"INSERT INTO Employees (CNIC, DeptID, Name, DateOfBirth, JoinDate, ContractEndDate, Email, phone, Salary) VALUES ('{CNIC}', '{dept}', '{Name}', '{dob}', '{join}', '{end}', '{email}', '{phone}', '{salary}')"
        # executeSQL(sql)
        
        print([x for x in request.POST.items()])
        try:
            executeSQL(sql)
            sql = fr"SELECT NumberOfEmployees FROM Department WHERE DeptID='{dept}'"
            total = int(executeSQL(sql, ['numberofemployees'])[0]['numberofemployees'])
            total = total + 1
            strdept = str(dept)
            sql = f"UPDATE Department SET NumberOfEmployees = {total} WHERE DeptID='{strdept}'"
            executeSQL(sql)
        except:
            return render(request, 'myadmin/cnic_exists.html', {"nav": which_nav(request)})
        
    return render(request, 'myadmin/addemployee.html', {"nav": which_nav(request)})

