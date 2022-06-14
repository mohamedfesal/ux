from flask import Blueprint, redirect, render_template, request, session, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from uxapp.config import admin_role_required, allowed_image_file
from uxapp.models import Users, Agents, Department, wfh_pcs
from uxapp import db
from uxapp.config import allowed_file
import pandas as pd 


#================================
# Blueprint For Users Managment
#================================

users_routes = Blueprint('users_routes', __name__)



#=========================
# Main Rout "LOGIN"
#=========================
@users_routes.route("/", methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect('/dashboard')
          
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()
        next = request.args.get('next')
        if user:
           
            # check if user is valid and statue is active
            if check_password_hash(user.password, password) and user.statue == 1:  
                login_user(user)
                flash('Logged in successfully.', 'alert-success')
                # Store user_id in session for socketio use
                session['user_id'] = current_user.id
                if user.user_depart.dep_name == 'TL':
                    return redirect(url_for('users_routes.tlteam', id = current_user.id))
                else:
                    return redirect(next or url_for('main.dashboard')) 
            elif user.statue == 0:
                flash('You account is not active, please refere to IT department to activate your account.', 'alert-danger') 
            else:
                flash('Invalid Email Or Password', 'alert-danger')
                return redirect(next or url_for('main.dashboard'))           
        else:
            flash('Invalid Email Or Password', 'alert-danger')  
            return redirect(next or url_for('main.dashboard'))            
        return redirect('/')
    
    return render_template("index.html", title="UX Centers - Login", companyName="UX Centers")

#=========================
# Users Profiles Route
#=========================
@users_routes.route("/profile/<int:id>" , methods=['GET', 'POST'])
@login_required
def profile(id):
    try: 
        user = Users.query.filter_by(id = id).first()
        return render_template('profile.html', title = user.username, user = user)
    except:
        return render_template('404.html'), 404  
#=========================
# Users Managment Route
#=========================
@users_routes.route("/users-managment" , methods=['GET', 'POST'])
@login_required
@admin_role_required
def users_mgm():
    if request.method == "POST":
        if 'add-user-form' in request.form:
            bio = request.form['add-bio']
            username = request.form['username']
            f_name = request.form['f-name']
            l_name = request.form['l-name']
            email = request.form['add-email']
            password = generate_password_hash(request.form['add-pass'], method = 'sha256')
            role = request.form['add-role']
            depart = request.form['add-dep']
            user = Users.query.filter_by(email=email).first()
            bio_check = Agents.query.filter_by(bio = bio).first()
            if user and user.bio != None:
                flash('User Already Exist', 'alert-danger')
            elif bio_check == None:
                flash('This User Not Exist in HC', 'alert-danger')
            else:
                addUser = Users(bio = bio, username = username,f_name =f_name, l_name = l_name, email = email, password = password, statue = 1, date_created = datetime.datetime.today(), role = role, depart = depart)
                db.session.add(addUser)
                db.session.commit()
                flash('User Aded', 'alert-success')
                return redirect(url_for('users_routes.users_mgm'))
        elif 'edit-user-form' in request.form:
            user_id = request.form['user-id']
            # print(user_id)
            bio = request.form['edit-bio']
            username = request.form['username']
            f_name = request.form['f-name']
            l_name = request.form['l-name']
            email = request.form['edit-email']
            if request.form['edit-pass'] != '':
                password = generate_password_hash(request.form['edit-pass'], method = 'sha256')
            role = request.form['edit-role']
            depart = request.form['edit-dep']
            stat= request.form.get('user-stat')
            # print(stat)
            user = Users.query.filter_by(id=user_id).first()
            try:
                user.bio = bio
                user.username = username
                user.f_name =f_name
                user.l_name = l_name
                user.email = email
                if request.form['edit-pass'] != '':
                    user.password = password
                if stat == 'on':
                    user.statue = 1
                else:
                    user.statue = 0
                user.role = role
                user.depart = depart
                db.session.commit()
                flash('User Updated Successfully', 'alert-success')
                return redirect(url_for('users_routes.users_mgm'))
            except:
                flash('Something went wrong! please try agian', 'alert-danger')
                return redirect(url_for('users_routes.users_mgm'))
        elif 'import-users' in request.form:
             file = request.files.get('sheet')
             if file and allowed_file(file.filename):
                if file.filename != '':
                    read_data = pd.read_excel(file)
                    data = read_data.fillna('')
                    excel_values = data.values.tolist()
                    for value in excel_values:
                        password = generate_password_hash('123456', method = 'sha256')
                        role = value[4]
                        depart = Department.query.filter_by(dep_name=value[3]).first()
                        user = Users.query.filter_by(email = value[2]).first()
                        bio_check = Agents.query.filter_by(bio = value[0]).first()
                        if user and user.bio != None:
                            flash('User Already Exist %s', 'alert-danger')%value[0]
                            
                        elif bio_check == None:
                            flash('This User Not Exist in HC %s', 'alert-danger')%value[0]
                            
                        else:
                            addUser = Users(bio = value[0], username = value[1],f_name =value[1].split(' ')[0], l_name = value[1].split(' ', 1)[1], email = value[2], password = password, statue = 1, date_created = datetime.datetime.today(), role = role, depart = depart.id)
                            db.session.add(addUser)
                            db.session.commit()
                flash('Users Imported', 'alert-success')
    elif request.method == "GET":
        id = request.args.get('userid')
        # print(id)
        if id != None:
            try:
                user_to_delete = Users.query.get(id)
                db.session.delete(user_to_delete)
                db.session.commit()
                flash('User has been deleted successfully', 'alert-success')
            except:
                flash('somthing went wrong, please try again', 'alert-danger')
    view_users = Users.query.order_by(Users.id)
    view_dep = Department.query.order_by(Department.id)
    return render_template("/users-mgm.html", title="Users Managment", usermgm = 'active',  view_users =  view_users, view_dep = view_dep)
#=========================
# Edit Profile Informaion Route
#=========================
@users_routes.route("/profile-info" , methods=['GET', 'POST'])
@login_required
def profile_info():
    if request.method == "POST":
        upload_file = request.files.get('avatar')
        # print(upload_file)
        user_id = current_user.id
        f_name = request.form['f-name']
        l_name = request.form['l-name']
        address = request.form['address']
        phone = request.form['phone']
        user = Users.query.filter_by(id = user_id).first()
        if upload_file.filename != '':
            extension=upload_file.filename.split(".")
            extension=str(extension[1])
            if upload_file and allowed_image_file(upload_file.filename):
                if upload_file.filename != '':
                    file_path = os.path.join(users_mgm.config["UPLOAD_AVATARS_FOLDER"], 'avatar-'+str(current_user.id)+ '.' + extension)
                    upload_file.save(file_path)
            else:
                flash('extention not allowed', 'alert-danger')        
        try:
            user.f_name = f_name
            user.l_name = l_name
            user.address = address
            user.phone = phone
            if upload_file.filename != '':
                user.avatar = file_path
            db.session.commit()
            flash('Profile Updated Successfully', 'alert-success')
            return redirect(request.referrer)
        except:
            flash('Something went wrong! please try agian', 'alert-danger')
            return redirect(request.referrer)
#=========================
# TL Team Route
#=========================
@users_routes.route("/my-team")
@login_required
def tlteam():
    team = wfh_pcs.query.filter(wfh_pcs.tl == current_user.id, wfh_pcs.agent != None).all()
   
    return render_template("/profiles/tl-team.html", title="My Team", tlteam = 'active', team = team)
#=========================
# Logout Route
#=========================
@users_routes.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')
   