import os
from os.path import join, dirname, realpath
from flask import request, redirect, flash
from sqlalchemy import create_engine
from flask_login import current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from functools import wraps



#=========================
# App Configs
#=========================
engine = create_engine('mysql+pymysql://root:@127.0.0.1/uxcdb')
class Config:
    SECRET_KEY =  os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@127.0.0.1/uxcdb'
    SQLALCHEMY_TRACK_MODIFICATION = True
    UPLOAD_FOLDER="static/uploads/excel"
    UPLOAD_RSA_FOLDER= join(dirname(realpath(__file__)), "static/uploads/tokens/")
    UPLOAD_AVATARS_FOLDER="static/uploads/avatars"
    DOWNLOAD_FOLDER="static/download"
    # Mail Init
    DEBUG = True
    TESTING = False
    MAIL_SERVER = 'smtp-mail.outlook.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'it-support-alex@uxcenters.com'
    MAIL_PASSWORD = 'UXC@!TAlex.2021'
    # MAIL_DEFAULT_SENDER'] = ('UXC App Notifications','mohamedfesal99@gmail.com')
    MAIL_MAX_EMAILS = None

#================================
# Admin Access Required Function
#================================
EXEMPT_METHODS = set(['OPTIONS'])
def admin_role_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_user.role != 1:
            flash('Access Denied, Admins only can view this page!', 'alert-danger')
            return redirect(request.referrer)
        return func(*args, **kwargs)
    return decorated_view

#=============================
# Allowed Files For Uploading
#=============================
# Allowed for Excel Files
ALLOWED_EXTENSIONS = {'xlsx'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Allowed for image Files
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg','jpeg'}
def allowed_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
# Allowed for RSA Files
ALLOWED_RSA_EXTENSIONS = {'sdtid'}
def allowed_rsa_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_RSA_EXTENSIONS
