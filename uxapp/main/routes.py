from flask import Blueprint, redirect, render_template, request, session, url_for, flash, jsonify
from flask_login import login_required
import datetime
from sqlalchemy import desc, extract
from uxapp.models import Users, wfh_pcs, Todolist

main = Blueprint('main', __name__)

#=========================
# Dashboard Route
#=========================
@main.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    dbusers = Users.query.order_by(Users.email)  
    # Statistics Queries 
    wfh_today = wfh_pcs.query.filter(wfh_pcs.wfhdate == datetime.datetime.today().strftime('%Y-%m-%d')).count()
    wfh_this_month = len(wfh_pcs.query.filter(extract('month', wfh_pcs.wfhdate) >= datetime.datetime.today().month,
                                extract('year', wfh_pcs.wfhdate) >= datetime.datetime.today().year).all())
    # print(len(wfh_this_month))
    if datetime.datetime.today().month == 1:
        l_month = 12
        l_year = datetime.datetime.today().year - 1
    else:
        l_month = datetime.datetime.today().month - 1
        l_year = datetime.datetime.today().year
    # print(l_month, l_year)
    wfh_last_month= len(wfh_pcs.query.filter(extract('month', wfh_pcs.wfhdate) >= l_month,
                                extract('year', wfh_pcs.wfhdate) >= l_year).all())
    wfh_this_year = len(wfh_pcs.query.filter(extract('year', wfh_pcs.wfhdate) >= datetime.datetime.today().year).all())
    wfh_last_year = len(wfh_pcs.query.filter(extract('year', wfh_pcs.wfhdate) == datetime.datetime.today().year - 1).all())
    # print(datetime.datetime.today().year - 1)
    
    return render_template("/dashboard.html", title="Dashboard", dashboard="active", dbusers = dbusers, wfh_today = wfh_today, wfh_this_month = wfh_this_month, wfh_last_month = wfh_last_month, wfh_this_year =wfh_this_year, wfh_last_year = wfh_last_year )

