from turtle import title
from flask import request, url_for
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from uxapp import db, login_manager
from flask_humanize import humanize
from flask_admin import Admin
from uxapp import admin

from flask_admin.contrib.sqla import ModelView
import datetime

# Login Manager 
@login_manager.user_loader
def get(id):
    return Users.query.get(id)
# Notifications

class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250))  
    body = db.Column(db.String(250))  
    action = db.Column(db.String(250)) 
    received_at = db.Column(db.DateTime)
    user = db.Column('user_notif_id', db.Integer, db.ForeignKey('users.id'))
    

#=========================
# Users Model
#=========================
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    bio = db.Column(db.Integer)
    username = db.Column(db.String(100), nullable = False)
    f_name = db.Column(db.String(100), nullable = False)
    l_name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(120), nullable= False, unique = True)
    password = db.Column(db.String(250), nullable = False)
    statue = db.Column(db.Integer)
    role = db.Column(db.Integer, nullable = False)
    date_created = db.Column(db.DateTime)
    depart = db.Column(db.Integer, db.ForeignKey('department.id'))
    address = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    task = db.relationship('Todolist', backref= 'user_task')
    avatar = db.Column(db.String(250))
    req_user = db.relationship('Requests', backref= 'user_req')
    user_team = db.relationship('wfh_pcs', backref= 'user_team')
    user_notifications = db.relationship('Notifications', backref= 'user_notifi')
    # def get_unread_notifs(self, reverse=False):
    #     notifs = []
    #     unread_notifs = Notifications.query.filter_by(user=self, has_read=False)
    #     for notif in unread_notifs:
    #         notifs.append({
    #             'title': notif.title,
    #             'received_at': humanize.naturaltime(datetime.now() - notif.received_at),
    #             'mark_read': url_for('profile.mark_notification_as_read', notification_id=notif.id)
    #         })

    #     if reverse:
    #         return list(reversed(notifs))
    #     else:
    #         return notifs

#==================================
# Department Model
#==================================
class Department(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    dep_name = db.Column(db.String(100), nullable = False)
    user = db.relationship('Users', backref='user_depart')
    request = db.relationship('Requests', backref='req_depart')
#==================================
# Agents (Headcount) Model
#==================================
class Agents(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    bio = db.Column(db.Integer)
    name = db.Column(db.String(100), nullable = False)
    l_name = db.Column(db.String(100), nullable = False)
    start_date = db.Column(db.DateTime)
    depart = db.Column(db.String(100))
    job_title = db.Column(db.String(100))
    email = db.Column(db.String(120))
    address = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    wfhpc = db.relationship('wfh_pcs', backref='agentpc')
    agstock = db.relationship('Stock', backref='agentstock')
    agent_dep = db.relationship('Departure', backref= 'agent_dep_req')
    tl = db.Column(db.String(100))
    tl_email = db.Column(db.String(100))
#==================================
# Agents (Headcount) Model
#==================================
class Leavers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    bio = db.Column(db.Integer)
    name = db.Column(db.String(100), nullable = False)
    l_name = db.Column(db.String(250), nullable = False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    depart = db.Column(db.String(100))
    job_title = db.Column(db.String(100))
    email = db.Column(db.String(120))
    address = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    reason = db.Column(db.String(250))
    sub_reason = db.Column(db.String(250))
    departure_type = db.Column(db.String(250))
    manager = db.Column(db.String(250))
#=========================
# PCs Details Model
#=========================
class pcs(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    site = db.Column(db.String(100))
    build = db.Column(db.String(100))
    floor = db.Column(db.String(100))
    station = db.Column(db.String(100))
    hostname= db.Column(db.String(250), nullable = True, unique = True)
    ip = db.Column(db.String(100), nullable = True, unique = True)
    pbxuser = db.Column(db.String(250),nullable = True, unique = True)
    ciscodid = db.Column(db.String(250),nullable = True, unique = True)
#=========================
# WFH PCs Table Model
#=========================
class wfh_pcs(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    station = db.Column(db.String(100))
    hostname= db.Column(db.String(250), nullable = True, unique = True)
    pbxuser = db.Column(db.String(250),nullable = True, unique = True)
    ciscodid = db.Column(db.String(250),nullable = True, unique = True)
    wfhdate = db.Column(db.DateTime)
    dlv_by = db.Column(db.String(100))
    agent = db.Column(db.Integer, db.ForeignKey('agents.id'))
    tl = db.Column(db.Integer, db.ForeignKey('users.id'))
    token = db.Column(db.String(250))
#=====================================
# Returned WFH Tracker Model
#=====================================
class Returned(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    r_agent = db.Column(db.String(250), nullable = False)
    r_agent_bio = db.Column(db.String(250), nullable = False)
    r_pc = db.Column(db.String(250), nullable = False)
    pc_statue = db.Column(db.String(250), nullable = False)
    screens_statue = db.Column(db.String(250), nullable = False)
    headset_statue = db.Column(db.String(250), nullable = False)
    hdd_statue = db.Column(db.String(250), nullable = False)
    r_date = db.Column(db.DateTime)
    ckecked_by = db.Column(db.String(250), nullable = False)
    comment = db.Column(db.String(250), default = "No Comments!")
#=====================================
# Stock Model
#=====================================

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    item_name = db.Column(db.String(100))
    serial = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    position = db.Column(db.String(100))
    comment = db.Column(db.String(250))
    assigned_to = db.Column(db.Integer, db.ForeignKey('agents.id'))
    stock_categ = db.Column(db.Integer, db.ForeignKey('stock_cat.id'))
    stock_order = db.Column(db.Integer, db.ForeignKey('orderingitems.id'))
    # add order history quantity to table
class Stock_cat(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    categ = db.Column(db.String(100))
    cat_icon = db.Column(db.String(10))
    stockRe_parent = db.relationship('Stock', backref= 'stock_item')
#=====================================
# Delivery Orders Model
#=====================================
class Orders(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250))
    date = db.Column(db.DateTime)
    items = db.relationship('Orderingitems', backref='view_items')

class Orderingitems(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    deliveryNote = db.Column(db.Integer, db.ForeignKey('orders.id'))
    items = db.relationship('Stock', backref ='view_stock_item')
    quantity = db.Column(db.Integer)


#=====================================
# ToDo Model
#=====================================
class Todolist(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String(250))
    date_created = db.Column(db.DateTime)
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    todo_statues = db.Column(db.Integer)
#=====================================
# Requests Model
#=====================================
class Requests(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    req_type = db.Column('req_type', db.Integer, db.ForeignKey('reqtype.id'))
    req_title = db.Column(db.String(100))
    req_date = db.Column(db.DateTime)
    req_by = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    dep_req = db.Column('dep_id', db.Integer, db.ForeignKey('departure.id'))
    depart_req = db.Column('depart_id', db.Integer, db.ForeignKey('department.id'))
    ticket_req = db.Column('tick_id', db.Integer, db.ForeignKey('tickets.id'))
    statue = db.Column(db.String(50))
#=====================================
# Tickets Categories Model
#=====================================  
class Ticket_cat(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    cat_parent = db.relationship('Ticket_subcat', backref= 'ticket_cat_parent')

#=====================================
# Tickets Sub Categories Model
#=====================================  
class Ticket_subcat(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    sub_cat = db.Column('ticket_cat_id', db.Integer, db.ForeignKey('ticket_cat.id'))
    cat_ticket = db.relationship('Tickets', backref= 'tickets_cat')
    
#=====================================
# Tickets Model
#=====================================
class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    sub_service = db.Column('ticket_sub_cat', db.Integer, db.ForeignKey('ticket_subcat.id'))
    impact = db.Column(db.String(100))
    urgency = db.Column(db.String(100))
    description = db.Column(db.String(250))
    req_ticket = db.relationship('Requests', backref= 'tickets_req')
#=====================================
# Requists type Model
#=====================================
class Reqtype(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    req_type = db.Column(db.String(100))
    request =  db.relationship('Requests', backref= 'r_type')
#=====================================
# Deprture Model
#=====================================
class Departure(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    agent = db.Column('agent_id', db.Integer, db.ForeignKey('agents.id'))
    facility_check = db.Column('facility_id', db.Integer, db.ForeignKey('facilitycheck.id'))
    it_check = db.Column('it_id', db.Integer, db.ForeignKey('itcheck.id'))
    security_check = db.Column('security_id', db.Integer, db.ForeignKey('securitycheck.id'))
    statue = db.Column(db.String(50))
    
## Facility Check List
class Facilitycheck(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    req_no = db.Column(db.String(250))
    pc = db.Column('pc',db.Boolean, unique=False, default=False)
    screens = db.Column('screens', db.Boolean, unique=False, default=False)
    desktop = db.Column('desktop', db.Boolean, unique=False, default=False)
    labtop = db.Column('labtop', db.Boolean, unique=False, default=False)
    cebox = db.Column('cebox', db.Boolean, unique=False, default=False)
    jack = db.Column('jack', db.Boolean, unique=False, default=False)
    usb = db.Column('usb', db.Boolean, unique=False, default=False)
    rj11 = db.Column('rj11', db.Boolean, unique=False, default=False)
    on_cell = db.Column('oncell', db.Boolean, unique=False, default=False)
    proffess = db.Column('proffess', db.Boolean, unique=False, default=False)
    locker = db.Column('locker', db.Boolean, unique=False, default=False)
    office = db.Column('office', db.Boolean, unique=False, default=False)
    comment = db.Column('comment', db.String(250))
    facility_dep = db.relationship('Departure', backref= 'f_dep_req')

## IT Check List
class Itcheck(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    req_no = db.Column(db.String(250))
    access = db.Column('access', db.Boolean, unique=False, default=False)
    internal_email = db.Column('internalEmail', db.Boolean, unique=False, default=False)
    external_email = db.Column('externalEmail', db.Boolean, unique=False, default=False)
    vpn = db.Column('vpn', db.Boolean, unique=False, default=False)
    comment = db.Column('comment', db.String(250))
    it_dep = db.relationship('Departure', backref= 'it_dep_req')

## Security Check List
class Securitycheck(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    req_no = db.Column(db.String(250))
    v_access = db.Column(db.Integer)
    security_dep = db.relationship('Departure', backref= 'sec_dep_req')

class Leaves(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(100))
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    approval = db.Column(db.Boolean, unique=False, default=False)
