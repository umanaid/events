from flask import Flask,render_template,redirect,request,url_for,flash,abort,session,Response,jsonify
import mysql.connector
from datetime import datetime
from flask_session import Session
from itsdangerous import URLSafeTimedSerializer
from key import salt,secret_key,salt2,salt3
from stoken import token
from cmail import sendmail
from otp import genotp
import os
import re
import stripe
# import pdfkit
#stripe.api_key='sk_test_51MMsHhSGj898WTbYXSx509gD14lhhXs8Hx8ipwegdytPB1Bkw0lJykMB0yGpCux95bdw1Gk9Gb9nJIWzPEEDxSqf00GEtCqZ8Y'
app=Flask(__name__)
app.secret_key=b'\xdaA\xd7ZJA\x0c\xb6w\x18@\xb6'
# config=pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
mydb=mysql.connector.connect(host="localhost",user="root",password="umanaidu",db='event')
app.config['SESSION_TYPE']='filesystem'
Session(app)
@app.route('/')
def index():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from vendors')


    count=cursor.fetchall()
    print(count)      
    cursor.close()
    return render_template('welcome.html',count=count)
@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        user=request.form['username']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['address']
        password=request.form['password_hash']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from users where username=%s',[user])
            count=cursor.fetchone()[0]
            #print(count)
            if count == 1:
                raise Exception
        except Exception as e:
            flash('user already existed')
            return redirect(url_for('login'))
        else:
            data={'username':user,'mobile':mobile,'email':email,'address':address,'password_hash':password}
            subject='The Confirmation Link For Event Planning Website'
            body=f"Click on the link to confirm {url_for('confirm',token=token(data,salt=salt),_external=True)}"
            sendmail(to=email,subject=subject,body=body)
            flash('Verfication link has sent to email')
            return redirect(url_for('login'))    
    return render_template('signup.html')
@app.route('/confirm/<token>')
def confirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
        abort(404,'link expired')
    else:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into users(username,password_hash,email,mobile,address) values(%s,%s,%s,%s,%s)',[data['username'],data['password_hash'],data['email'],data['mobile'],data['address']])
        mydb.commit()
        cursor.close()
        flash('Your details has registered successfully')
        return redirect(url_for('login'))
@app.route('/login',methods=['GET','POST'])
def login():
    if session.get('user'):
        return redirect(url_for('home'))
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from users where username=%s and password_hash=%s',[username,password])
            count=cursor.fetchone()[0]
            print(count)
            if count==0:
                raise Exception
        except Exception as e:
            flash('username or password are incorrect')
            return redirect(url_for('login'))
        else:
            session['user']=username
            print(session.get('user'))
            if not session.get(username):
                session[username]={}
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('login'))
    return redirect(url_for('login'))
@app.route('/forget',methods=['GET','POST'])
def forgot():
    if request.method=='POST':
        email=request.form['email']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from users where email=%s',[email])
        count=cursor.fetchone()[0]
        cursor.close()
        try:
            if count != 1:
                raise Exception
        except Exception as e:
            flash('pls register first')
            return redirect(url_for('signup'))
        else:
            subject='The password Reset link has sent to your email'
            body=f"The link password reset is: {url_for('verify',token=token(email,salt=salt2),_external=True)}"
            sendmail(to=email,subject=subject,body=body)
            flash('The Reset link has sent mail pls verify it')
            return redirect(url_for('forgot'))
    return render_template('forgot.html')
@app.route('/verify/<token>',methods=['GET','POST'])
def verify(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt2,max_age=180)
    except Exception as e:
        abort(404,'link expired')
    else:
        if request.method=='POST':
            npassword=request.form['npassword']
            cpassword=request.form['cpassword']
            if npassword==cpassword:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('update users set password_hash=%s where email=%s',[npassword,data])
                mydb.commit()
                cursor.close()
                flash('password has been updated')
                return redirect(url_for('login'))
            else:
                flash('Mismatched password confirmation')
                return render_template('newpassword.html')
    return render_template('newpassword.html')
@app.route('/vsignup',methods=['GET','POST'])
def vsignup():
    if request.method=='POST':
        vendor=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['address']
        password=request.form['password']
        services=request.form.getlist('Services')
        services=','.join(services)
        img=request.files['profile_pic']
        filename=img.filename
        print(filename)
        path=os.path.dirname(os.path.abspath(__file__))
        static_path=os.path.join(path,'static')
        img.save(os.path.join(static_path,filename))
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from vendors where name=%s',[vendor])
            count=cursor.fetchone()[0]
            print(count)
            if count == 1:
                raise Exception
        except Exception as e:
            flash('Vendor already existed')
            return redirect(url_for('vlogin'))
        else:
            data={'vendor':vendor,'mobile':mobile,'email':email,'address':address,'password':password,'services':services,'filename':filename}
            subject='The Confirmation Link For Event Planning Website'
            body=f"Click on the link to confirm {url_for('vconfirm',token=token(data,salt=salt),_external=True)}"
            sendmail(to=email,subject=subject,body=body)
            flash('Verfication link has sent to email')
            return redirect(url_for('vsignup'))    
    return render_template('vsignup.html')
@app.route('/vconfirm/<token>')
def vconfirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
        abort(404,'link expired')
    else:
        print(data['services'])
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into vendors(name,mobile,email,address,password,services,filename) values(%s,%s,%s,%s,%s,%s,%s)',[data['vendor'],data['mobile'],data['email'],data['address'],data['password'],data['services'],data['filename']])
        mydb.commit()
        cursor.close()
        flash('Your details has registered successfully')
        return redirect(url_for('vlogin'))
@app.route('/vhome')
def vhome():
    if session.get('vendor'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select vendor_id from vendors where name=%s',[session.get('vendor')])
        data=cursor.fetchone()[0]
        cursor.close()
        return render_template('vhome.html',data=data)
    else:
        return redirect(url_for('vlogin'))
@app.route('/vlogin',methods=['GET','POST'])
def vlogin():
    if session.get('vendor'):
        return redirect(url_for('vhome'))
    if request.method=='POST':
        vendorname=request.form['name']
        password=request.form['password']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from vendors where name=%s and password=%s',[vendorname,password])
            count=cursor.fetchone()[0]
            print(count)
            if count==0:
                raise Exception
        except Exception as e:
            flash('vendorname or password are incorrect')
            return redirect(url_for('vlogin'))
        else:
            session['vendor']=vendorname
            if not session.get(vendorname):
                session[vendorname]={}
            return redirect(url_for('vhome'))
    return render_template('vlogin.html')

@app.route('/vlogout')
def vlogout():
    if session.get('vendor'):
        session.pop('vendor')
        return redirect(url_for('vlogin'))
    return redirect(url_for('vlogin'))
@app.route('/vforgot',methods=['GET','POST'])
def vforgot():
    if request.method=='POST':
        email=request.form['email']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from vendors where email=%s',[email])
        count=cursor.fetchone()[0]
        cursor.close()
        try:
            if count != 1:
                raise Exception
        except Exception as e:
            flash('pls register first')
            return redirect(url_for('vsignup'))
        else:
            subject='The password Reset link has sent to your email'
            body=f"The link password reset is: {url_for('vverify',token=token(email,salt=salt2),_external=True)}"
            sendmail(to=email,subject=subject,body=body)
            flash('The Reset link has sent mail pls verify it')
            return redirect(url_for('vforgot'))
    return render_template('vforgot.html')
@app.route('/vverify/<token>',methods=['GET','POST'])
def vverify(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt2,max_age=180)
    except Exception as e:
        abort(404,'link expired')
    else:
        if request.method=='POST':
            npassword=request.form['npassword']
            cpassword=request.form['cpassword']
            if npassword==cpassword:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('update vendors set password=%s where email=%s',[npassword,data])
                mydb.commit()
                cursor.close()
                flash('password has been updated')
                return redirect(url_for('login'))
            else:
                flash('Mismatched password confirmation')
                return render_template('newpassword.html')
    return render_template('newpassword.html')
@app.route('/profile/<type>',methods=['GET','POST'])
def profile(type):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select vendor_id,name,mobile,email,services,filename from vendors where vendor_id=%s',[type])
    count=cursor.fetchone()
    print('**************************88',count)
    cursor.close()
    return render_template("contactus.html",count=count)
@app.route('/update_profile/<type>',methods=['GET','POST'])
def update_profile(type):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select vendor_id,name,mobile,email,services,filename from vendors where vendor_id=%s',[type])
    count=cursor.fetchone()
    print(count)
    if request.method=='POST':
        vendor=request.form['vendor_name']
        mobile=request.form['mobile']
        email=request.form['email']
        services=request.form['services']

        if request.files['profile_pic'].filename=='':
                print('hi')
                filename=count[3]
        else:
            img=request.files['profile_pic']
            filename=img.filename
            print(filename)
            path=os.path.dirname(os.path.abspath(__file__))
            static_path=os.path.join(path,'static')
            img.save(os.path.join(static_path,filename))
        try:
            cursor.execute('update vendors set name=%s,mobile=%s,email=%s,services=%s,filename=%s where vendor_id=%s',[vendor,mobile,email,services,filename,type])
            mydb.commit()
            cursor.close()
        except Exception as e:
            print(e)
        return redirect(url_for('update_profile',type=type))

    return render_template("update_profile.html",count=count)


@app.route('/events',methods=['GET','POST'])
def events():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from users where user_id=(select user_id from users where username=%s)',[session.get('user')])
    count=cursor.fetchone()
    print(count)
    cursor.close()
    return render_template('events.html',count=count)
@app.route('/eventdetails/<user>',methods=['GET','POST'])
def eventdetails(user):
    if session.get('user'):
        if request.method=='POST':
            name=request.form['purpose']
            date=request.form['date']
            time=request.form['time']
            
            location=request.form['location']
            description=request.form['description']
            #availability=request.form['calender_integration']
            services=request.form.getlist('Services')
            services=','.join(services)
            path=os.path.dirname(os.path.abspath(__file__))
            static_path=os.path.join(path,'static')
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into events(user_id,title,date,time,location,description,services) values(%s,%s,%s,%s,%s,%s,%s)',[user,name,date,time,location,description,services])
            mydb.commit()
            cursor.close()
            flash('Deatils submited successfully')
            return redirect(url_for('events'))
    return render_template('eventdetails.html')
# @app.route('/services',methods=['GET','POST'])
# def services():
#     return render_template('services.html')
# @app.route('/viewcontactus')
# def viewcontactus():
#     cursor=mydb.cursor(buffered=True)
#     cursor.execute('select * from contactus')
#     reports=cursor.fetchall()
#     cursor.close()
#     return render_template('viewcontactus.html',reports=reports)
@app.route('/showevents/<userid>')
def showevents(userid):
    if session.get('user'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from events where user_id=%s',[userid])
        events=cursor.fetchall()
        print(events)
        cursor.close()
        return render_template('showevents.html',events=events)
    else:
        return redirect(url_for('events'))
@app.route('/catering/<types>',methods=['GET','POST'])
def catering(types):
    if session.get('vendor'):
        if request.method=='POST':
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select vendor_id from vendors where name=%s',[session.get('vendor')])
            data=cursor.fetchone()[0]
            cursor.close()
            img=request.files['catering']
            capacity=request.form['capacity']
            budget=request.form['min_budget']
            filename=genotp()+'.jpg'
            path=os.path.dirname(os.path.abspath(__file__))
            static_path=os.path.join(path,'static')
            img.save(os.path.join(static_path,filename))
            print(data,types,filename,capacity)
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into vendor_services(vendor_id,service,provided_services,minimum_capacity,min_budget) values(%s,%s,%s,%s,%s)',[data,types,filename,capacity,budget])
            mydb.commit()
            cursor.close()
    return render_template('catering.html')
@app.route('/enter/<types>',methods=['GET','POST'])
def enter(types):
    if session.get('vendor'):
        if request.method=='POST':
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select vendor_id from vendors where name=%s',[session.get('vendor')])
            data=cursor.fetchone()[0]
            cursor.close()
            img=request.files['catering']
            budget=request.form['min_budget']
            capacity=request.form['capacity']
            filename=genotp()+'.jpg'
            path=os.path.dirname(os.path.abspath(__file__))
            static_path=os.path.join(path,'static')
            img.save(os.path.join(static_path,filename))
            print(data,types,filename,capacity)
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into vendor_services(vendor_id,service,provided_services,minimum_capacity,min_budget) values(%s,%s,%s,%s,%s)',[data,types,filename,capacity,budget])
            mydb.commit()
            cursor.close()
            return redirect(url_for('vhome'))
    return render_template('entertainment.html')
@app.route('/venue/<types>',methods=['GET','POST'])
def venue(types):
    if session.get('vendor'):
        if request.method=='POST':
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select vendor_id from vendors where name=%s',[session.get('vendor')])
            data=cursor.fetchone()[0]
            cursor.close()
            img=request.files['venue']
            capacity=request.form['capacity']
            budget=request.form['min_budget']
            filename=genotp()+'.jpg'
            path=os.path.dirname(os.path.abspath(__file__))
            static_path=os.path.join(path,'static')
            img.save(os.path.join(static_path,filename))
            print(data,types,filename,capacity)
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into vendor_services(vendor_id,service,provided_services,minimum_capacity,min_budget) values(%s,%s,%s,%s,%s)',[data,types,filename,capacity,budget])
            mydb.commit()
            cursor.close()
    return render_template('venue.html')
@app.route('/photography/<types>',methods=['GET','POST'])
def photography(types):
    if session.get('vendor'):
        if request.method=='POST':
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select vendor_id from vendors where name=%s',[session.get('vendor')])
            data=cursor.fetchone()[0]
            cursor.close()
            img=request.files['cards']
            capacity=request.form['capacity']
            budget=request.form['min_budget']
            filename=genotp()+'.jpg'
            path=os.path.dirname(os.path.abspath(__file__))
            static_path=os.path.join(path,'static')
            img.save(os.path.join(static_path,filename))
            print(data,types,filename,capacity)
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into vendor_services(vendor_id,service,provided_services,minimum_capacity,min_budget) values(%s,%s,%s,%s,%s)',[data,types,filename,capacity,budget])
            mydb.commit()
            cursor.close()
    return render_template('photography.html')
@app.route('/beauty/<types>',methods=['GET','POST'])
def beauty(types):
    if session.get('vendor'):
        if request.method=='POST':
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select vendor_id from vendors where name=%s',[session.get('vendor')])
            data=cursor.fetchone()[0]
            cursor.close()
            img=request.files['cards']
            capacity=request.form['capacity']
            budget=request.form['min_budget']
            filename=genotp()+'.jpg'
            path=os.path.dirname(os.path.abspath(__file__))
            static_path=os.path.join(path,'static')
            img.save(os.path.join(static_path,filename))
            print(data,types,filename,capacity)
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into vendor_services(vendor_id,service,provided_services,minimum_capacity,min_budget) values(%s,%s,%s,%s,%s)',[data,types,filename,capacity,budget])
            mydb.commit()
            cursor.close()
    return render_template('beauty.html')

@app.route('/deco/<types>',methods=['GET','POST'])
def deco(types):
    if session.get('vendor'):
        if request.method=='POST':
            img=request.files['catering']
            capacity=request.form['capacity']
            budget=request.form['min_budget']
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select vendor_id from vendors where name=%s',[session.get('vendor')])
            data=cursor.fetchone()[0]
            cursor.close()
            filename=genotp()+'.jpg'
            path=os.path.dirname(os.path.abspath(__file__))
            static_path=os.path.join(path,'static')
            img.save(os.path.join(static_path,filename))
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into vendor_services(vendor_id,service,provided_services,minimum_capacity,min_budget) values(%s,%s,%s,%s)',[data,types,filename,capacity,budget])
            mydb.commit()
            cursor.close()
            return redirect(url_for('vhome'))
    return render_template('deco.html')
@app.route('/props/<types>',methods=['GET','POST'])
def props(types):
    if session.get('vendor'):
        if request.method=='POST':
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select vendor_id from vendors where name=%s',[session.get('vendor')])
            data=cursor.fetchone()[0]
            cursor.close()
            img=request.files['catering']
            filename=genotp()+'.jpg'
            path=os.path.dirname(os.path.abspath(__file__))
            static_path=os.path.join(path,'static')
            img.save(os.path.join(static_path,filename))
            capacity=request.form['minimum_capacity']
            budget=request.form['min_budget']
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into vendor_services(vendor_id,service,provided_services,minimum_capacity,min_budget) values(%s,%s,%s,%s,%s)',[data,types,filename,capacity,budget])
            mydb.commit()
            cursor.close()
            return redirect(url_for('vhome'))
    return render_template('props.html')
@app.route('/invitations/<types>',methods=['GET','POST'])
def invitations(types):
    if session.get('vendor'):
        if request.method=='POST':
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select vendor_id from vendors where name=%s',[session.get('vendor')])
            data=cursor.fetchone()[0]
            cursor.close()
            img=request.files['cards']
            capacity=request.form['capacity']
            budget=request.form['min_budget']
            filename=genotp()+'.jpg'
            path=os.path.dirname(os.path.abspath(__file__))
            static_path=os.path.join(path,'static')
            img.save(os.path.join(static_path,filename))
            print(data,types,filename,capacity)
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into vendor_services(vendor_id,service,provided_services,minimum_capacity,min_budget) values(%s,%s,%s,%s,%s)',[data,types,filename,capacity,budget])
            mydb.commit()
            cursor.close()
    return render_template('invitations.html')
@app.route('/addtask/<e_id>',methods=['GET','POST'])
def addtask(e_id):
    if session.get('user'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select services,user_id from events where event_id=(%s)',[e_id])
        data=cursor.fetchall()
        print(data)
    for row in data:
        lst=row[0]
        id2=row[1]
        print(lst)
        l=[]
        for i in lst:
            cursor.execute('select vs.vendor_id,vs.service,vs.min_budget,v.name,provided_services from vendor_services vs join vendors v on vs.vendor_id=v.vendor_id where vs.service=%s', [i])
            count=cursor.fetchall()
            l.append(count)
    print(l)

    cursor.close()
    return render_template('addtask.html',l=l,e_id=e_id,id2=id2)
@app.route('/vendor_task',methods=['GET','POST'])
def vendor_tasks():
    if session.get('vendor'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('SELECT vendor_id FROM vendors WHERE name=%s', [session.get('vendor')])
        user_id = cursor.fetchone()[0]
        cursor.execute('select t.task_id,t.event_id,t.title,t.assigned_to,t.user_id,b.budget_id,b.total_budget,u.username from tasks t join budgets b on t.task_id=b.task_id join users u on t.user_id=u.user_id where t.assigned_to=%s',[user_id])
        data=cursor.fetchall()
        print(data)
        cursor.close()
    return render_template('vadded_task.html',data=data)
@app.route('/view_task/<title>/<e_id>',methods=['GET','POST'])
def view_task(title,e_id):
    if session.get('vendor'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select t.task_id,t.event_id,t.title,t.assigned_to,t.user_id,b.budget_id,b.total_budget,u.username,t.accept,t.completion_status,u.email from tasks t join budgets b on t.task_id=b.task_id join users u on t.user_id=u.user_id where title=%s and t.event_id=%s',[title,e_id])
        data=cursor.fetchall()
        print(data)
        cursor.close()
        if request.method=='POST':
            status=request.form['completion_status']
            accept = request.form['accept_status'] if not data[0][8] else data[0][8]
            cursor=mydb.cursor(buffered=True)
            cursor.execute('update tasks set completion_status=%s,accept=%s where task_id=%s',[status,accept,data[0][0]])
            mydb.commit()
            cursor.close()
            subject='Acception Mail'
            body=f"The Vendor {session.get('vendor')} has accepted your task {data[0][2]}"
            sendmail(to=data[0][10],subject=subject,body=body)
            flash('Your acception mail has sent to User')
            return redirect(url_for('view_task',title=title,e_id=e_id))
    return render_template('view_task.html',data=data)
@app.route('/task/<id1>/<e_id>/<title>',methods=['GET','POST'])
def task(id1,e_id,title):
    if session.get('user'):
        if request.method=='POST':
            try:
                description = request.form['description']
                deadline = request.form['deadline']
                
                budget=request.form['budget']
                cursor = mydb.cursor(buffered=True)
                cursor.execute('SELECT user_id FROM users WHERE username=%s', [session.get('user')])
                user_id = cursor.fetchone()[0]
                cursor.close()
                cursor=mydb.cursor(buffered=True)
                cursor.execute('insert into tasks(user_id,assigned_to,event_id,title,description,deadline) values(%s,%s,%s,%s,%s,%s)',[user_id,id1,e_id,title,description,deadline])
                cursor.execute('select task_id from tasks where event_id =%s and title = %s',[e_id,title])
                t_id=cursor.fetchone()[0]
                cursor.execute('insert into budgets(task_id,event_id,total_budget) values(%s,%s,%s)',[t_id,e_id,budget])
                mydb.commit()
                cursor.close()
                flash('Deatils submited successfully')
                return redirect(url_for('addtask',e_id=e_id))
            except Exception:
                flash('task has already assigned')
                return redirect(url_for('addtask',e_id=e_id))
    return render_template('assign_task.html',e_id=e_id)
@app.route('/message/<id1>/<e_id>/<title>', methods=['GET', 'POST'])
def message(id1,e_id,title):
    if session.get('vendor'):  # Allow both users and vendors
        if session.get('vendor'):
            user_type = 'sender'  # User is sender
        else:
            user_type = 'reviver'  # Vendor is receiver

        cursor = mydb.cursor(buffered=True)
        cursor.execute('SELECT vendor_id FROM vendors WHERE name=%s', [session.get('vendor')])
        user_id = cursor.fetchone()[0]
        cursor.execute("SELECT * from chat_messages WHERE (sender_id = %s AND receiver_id = %s and event_id=%s and title=%s) ORDER BY created_at", (id1,user_id,e_id,title))
        data = cursor.fetchall()
        
        
        cursor.execute("SELECT * from chat_messages WHERE (receiver_id = %s AND sender_id = %s and event_id=%s and title=%s) ORDER BY created_at", (id1,user_id,e_id,title))
        data1 = cursor.fetchall()
        messages=data+data1
        sender = [(msg[0], msg[1],msg[2],msg[3],msg[4],msg[5]) for msg in messages if msg[2] == user_id]
        receiver = [(msg[0], msg[1],msg[2],msg[3],msg[4],msg[5]) for msg in messages if msg[2] != user_id]
        
        if request.method == 'POST':
            message = request.form['Message']
            file=request.files['file']
            filename=genotp()+'.jpg'
            path=os.path.dirname(os.path.abspath(__file__))
            static_path=os.path.join(path,'static')
            file.save(os.path.join(static_path,filename))
            cursor.execute('INSERT INTO chat_messages (sender_id, receiver_id, message,file_path,event_id,title) VALUES (%s, %s, %s,%s,%s,%s)', (user_id,id1, message,filename,e_id,title))
            mydb.commit()
            cursor.execute("SELECT * from chat_messages WHERE (sender_id = %s AND receiver_id = %s and event_id=%s and title=%s) ORDER BY created_at", (id1,user_id,e_id,title))
            data = cursor.fetchall()
            
            cursor.execute("SELECT * from chat_messages WHERE (receiver_id = %s AND sender_id = %s and event_id=%s and title=%s) ORDER BY created_at", (id1,user_id,e_id,title))
            data1 = cursor.fetchall()
            cursor.close()
            messages=data+data1
            sender = [(msg[0], msg[1],msg[2],msg[3],msg[4],msg[5]) for msg in messages if msg[2] == user_id]
            receiver = [(msg[0], msg[1],msg[2],msg[3],msg[4],msg[5]) for msg in messages if msg[2] != user_id]
            return redirect(url_for('message', id1=id1,e_id=e_id,title=title))

        return render_template('chatting.html', sender=sender, receiver=receiver, sender_id=id1, receiver_id=user_id)
    return redirect(url_for('login'))
@app.route('/umessage/<id1>/<e_id>/<title>', methods=['GET', 'POST'])
def umessage(id1,e_id,title):
    if session.get('user'):  # Allow both users and vendors
        print(session.get('user'))
        cursor = mydb.cursor(buffered=True)
        cursor.execute('SELECT user_id FROM users WHERE username=%s', [session.get('user')])
        user_id = cursor.fetchone()[0]

        cursor.execute("SELECT * from chat_messages WHERE (sender_id = %s AND receiver_id = %s and event_id=%s and title=%s) ORDER BY created_at", (id1,user_id,e_id,title))
        data = cursor.fetchall()
        cursor.execute("SELECT * from chat_messages WHERE (receiver_id = %s AND sender_id = %s and event_id=%s and title=%s) ORDER BY created_at", (id1,user_id,e_id,title))
        data1 = cursor.fetchall()
        messages=data+data1
        sender = [(msg[0], msg[1],msg[2],msg[3],msg[4],msg[5]) for msg in messages if msg[2] == user_id]
        receiver = [(msg[0], msg[1],msg[2],msg[3],msg[4],msg[5]) for msg in messages if msg[2] != user_id]

        if request.method == 'POST':
            message = request.form['Message']
            file=request.files['file']
            filename=genotp()+'.jpg'
            path=os.path.dirname(os.path.abspath(__file__))
            static_path=os.path.join(path,'static')
            file.save(os.path.join(static_path,filename))
            cursor.execute('INSERT INTO chat_messages (sender_id, receiver_id, message,file_path,event_id,title) VALUES (%s, %s, %s,%s,%s,%s)', (user_id,id1, message,filename,e_id,title))
            mydb.commit()

            cursor.execute("SELECT * from chat_messages WHERE (sender_id = %s AND receiver_id = %s and event_id=%s and title=%s) ORDER BY created_at", (id1,user_id,e_id,title))
            data = cursor.fetchall()
            cursor.execute("SELECT * from chat_messages WHERE (receiver_id = %s AND sender_id = %s and event_id=%s and title=%s) ORDER BY created_at", (id1,user_id,e_id,title))
            data1 = cursor.fetchall()
            cursor.close()
            messages=data+data1
            sender = [(msg[0], msg[1],msg[2],msg[3],msg[4],msg[5]) for msg in messages if msg[2] == user_id]
            receiver = [(msg[0], msg[1],msg[2],msg[3],msg[4],msg[5]) for msg in messages if msg[2] != user_id]
            return redirect(url_for('umessage', id1=id1,e_id=e_id,title=title))

        return render_template('chatting.html', sender=sender, receiver=receiver, sender_id=user_id, receiver_id=id1)
    return redirect(url_for('login'))
@app.route('/customization_form/<id1>/<e_id>/<title>/<id2>')
def customization_form(id1,e_id,title,id2):
    return render_template('custom.html',id2=id2,id1=id1,e_id=e_id,title=title)

# Route to handle form submission and store data in the database
@app.route('/save_customization/<id1>/<e_id>/<title>/<id2>', methods=['POST'])
def save_customization(id1,id2,e_id,title):
    if request.method == 'POST':
        event_details_customization = request.form['event_details_customization']
        branding_customization = request.form['branding_customization']
        communication_templates_customization = request.form['communication_templates_customization']

        cursor = mydb.cursor()
        cursor.execute("INSERT INTO customization (event_details_customization, branding_customization, communication_templates_customization,event_id,title,user_id) VALUES (%s, %s, %s,%s,%s,%s)", (event_details_customization, branding_customization, communication_templates_customization,e_id,title,id2))
        mydb.commit()
        cursor.close()
        return redirect(url_for('addtask',e_id=e_id))
        
    else:
        return redirect(url_for('customization_form',id1=id1,e_id=e_id,title=title))
@app.route('/guests/<e_id>/<u_id>',methods=['GET','POST'])
def guests(e_id,u_id):
    if session.get('user'):
        if request.method=='POST':
            name=request.form['name']
            email=request.form['email']
            invitation=request.form['invitation']
            rsvp=request.form['rsvp']
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into guests(name,email,invitation_sent,rsvp_status,event_id) values(%s,%s,%s,%s,%s)',[name,email,invitation,rsvp,e_id])
            mydb.commit()
            cursor.close()
            flash('Deatils submited successfully')
            return redirect(url_for('showevents',userid=u_id))
    return render_template('guest.html')
@app.route('/view_guests',methods=['GET','POST'])
def view_guests():
    if session.get('vendor'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from guests')
        guests=cursor.fetchall()
        cursor.close()
        return render_template('view_guests.html',guests=guests)
    return redirect(url_for('vlogin'))
@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='POST':
        name=request.form['search']
        strg=['A-Za-z0-9']
        pattern=re.compile(f'^{strg}', re.IGNORECASE)
        if (pattern.match(name)):
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select vs.vendor_id,vs.service,vs.min_budget,v.name,provided_services,v.mobile from vendor_services vs join vendors v on vs.vendor_id=v.vendor_id where vs.service like %s', [name + '%'])
            data=cursor.fetchall()
            cursor.close()
            print('hi')
            return render_template('dashboard.html', l=data)
        else:
            flash('result not found')
    return render_template('home.html')
@app.route('/vsearch',methods=['GET','POST'])
def vsearch():
    if request.method=='POST':
        name=request.form['search']
        strg=['A-Za-z0-9']
        pattern=re.compile(f'^{strg}', re.IGNORECASE)
        if (pattern.match(name)):
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select t.task_id,t.event_id,t.title,t.assigned_to,t.user_id,b.budget_id,b.total_budget,u.username from tasks t join budgets b on t.task_id=b.task_id join users u on t.user_id=u.user_id where title like %s',[name + '%'])
            data=cursor.fetchall()
            print('hi')
            return render_template('vadded_task.html',data=data)
        else:
            flash('result not found')
    return render_template('home.html')
@app.route('/contactus')
def contactus():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select vs.vendor_id,vs.service,vs.min_budget,v.name,provided_services,v.mobile from vendor_services vs join vendors v on vs.vendor_id=v.vendor_id')
    data=cursor.fetchall()
    cursor.close()
    print('hi')
    return render_template('dashboard.html', l=data)
@app.route('/dashboard/<type>')
def dashboard(type):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select vs.vendor_id,vs.service,vs.min_budget,v.name,provided_services,v.mobile from vendor_services vs join vendors v on vs.vendor_id=v.vendor_id where vs.service=%s',[type])
    data=cursor.fetchall()
    cursor.close()
    print('hi')
    return render_template('dashboard.html', l=data)
@app.route('/view_customs/<title>/<e_id>',methods=['GET','POST'])
def view_customs(title,e_id):
    if session.get('vendor'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from customization where title=%s and event_id=%s',[title,e_id])
        guests=cursor.fetchall()
        cursor.close()
        return render_template('view_customs.html',guests=guests)

app.run(debug=True,use_reloader=True)