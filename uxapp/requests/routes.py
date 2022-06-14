from flask import Blueprint, redirect, render_template, request, session, url_for, flash, jsonify, send_file
from flask_login import login_required, current_user
from sqlalchemy import desc
import datetime
from uxapp.models import wfh_pcs, Agents, Itcheck,Facilitycheck, Departure, Requests, Securitycheck,Ticket_cat, Ticket_subcat, Tickets
from uxapp import db
req_routes = Blueprint('req_routes', __name__)

#=========================
# Requests Route
#=========================
@req_routes.route("/request" , methods=['GET', 'POST'])
@login_required
def requests():
    sub_id = request.form.get('service_id')
    ticket_cat = Ticket_cat.query.all()
    ticket_sub_cat = Ticket_subcat.query.filter_by(id = 1).all()
    if request.method == 'POST':
        title = request.form['title']
        if 'dep_req_form' in request.form:
            bio = request.form['bio']
            agent_qu = Agents.query.filter_by(bio = bio).first()
            if agent_qu:
                add_dep = Departure(agent = agent_qu.id)
                db.session.add(add_dep)
                db.session.flush()
                send_facility = Facilitycheck(req_no = add_dep.id)
                send_it = Itcheck(req_no = add_dep.id)
                send_security = Securitycheck(req_no = add_dep.id)
                add_request = Requests(dep_req = add_dep.id, req_title = title, req_date = datetime.datetime.today(), req_by = current_user.id, req_type = 1, depart_req = current_user.depart)
                db.session.add(add_request)
                db.session.add(send_facility)
                db.session.add(send_it)
                db.session.add(send_security)
                db.session.commit()
                flash('Request Created Successfully', 'alert-success')
            else:
                flash('Error, Make sure that the agent is exist', 'alert-danger')
        if 'new_ticket' in request.form:
            service = request.form.get('service_id')
            sub_service = request.form.get('servicesubcategory_id')
            impact = request.form.get('impact')
            urgency = request.form.get('urgency')
            t_title = request.form.get('title')
            description = request.form.get('description')
            if request.method == "POST":
                add_ticket = Tickets(sub_service = sub_service, impact = impact, urgency = urgency, title = t_title, description = description)
                db.session.add(add_ticket)
                db.session.flush()
                add_request = Requests(ticket_req = add_ticket.id, req_title = t_title, req_date = datetime.datetime.today(), req_by = current_user.id, req_type = 3, depart_req = current_user.depart)
                db.session.add(add_request)
                db.session.commit()

    # all_req = Departure.query.order_by(Departure.id).all()
    all_req = Requests.query.order_by(desc(Requests.id)).all()
    all_dep_req = Requests.query.filter_by(depart_req = current_user.depart).all()
    all_opend_req = Requests.query.filter_by(statue = None).all()
    all_resolved_req = Requests.query.filter_by(statue = 'resolved').all()
    all_closed_req = Requests.query.filter_by(statue = 'closed').all()
    tickets = Tickets.query.order_by(Tickets.id).all()
    return render_template("/requests.html", title="Requests", requests = 'active', all_req = all_req, all_opend_req = all_opend_req, all_closed_req= all_closed_req, all_resolved_req = all_resolved_req , all_dep_req = all_dep_req, ticket_cat = ticket_cat, ticket_sub_cat = ticket_sub_cat, tickets = tickets)
#======================
# Requests Edit Route
#======================
@req_routes.route("/request/<int:id>" , methods=['GET', 'POST'])
@login_required
def requests_edit(id):
    req = Requests.query.filter_by(id = id).first()
    dep = None
    have_pc = None
    if req.dep_req is not None:
        dep = Departure.query.filter_by(id = req.dep_req).first()
        have_pc = wfh_pcs.query.filter_by(agent = dep.agent).first()
    if request.method == 'POST':
        def req_check(to_check): # This function for generate True or False from form checkbox
            return True if to_check != None else False
        if 'facility-check' in request.form:
            edit_req = Facilitycheck.query.filter_by(req_no = dep.id).first()
            pc = request.form.get('pc')
            screens = request.form.get('screens')
            desktop = request.form.get('desktop')
            labtop = request.form.get('labtop')
            cebox = request.form.get('cebox')
            jack = request.form.get('jack')
            usb = request.form.get('usb')
            rj11 = request.form.get('rj11')
            on_cell = request.form.get('on-cell')
            proffess = request.form.get('proffess')
            locker = request.form.get('locker')
            office = request.form.get('office')
            comment = request.form.get('comment')
            # print(req_check(screens))
            try:
                edit_req.pc = req_check(pc)
                edit_req.screens = req_check(screens)
                edit_req.desktop = req_check(desktop)
                edit_req.labtop = req_check(labtop)
                edit_req.cebox = req_check(cebox)
                edit_req.jack = req_check(jack)
                edit_req.usb = req_check(usb)
                edit_req.rj11 = req_check(rj11)
                edit_req.on_cell = req_check(on_cell)
                edit_req.proffess = req_check(proffess)
                edit_req.locker = req_check(locker)
                edit_req.office = req_check(office)
                edit_req.comment = comment
                dep.facility_check = edit_req.id
                if dep.it_check != None or dep.it_check != '':
                    dep.statue = 'resolved'
                    req.statue = 'resolved'
                db.session.commit()
                flash('Request Updated', 'alert-success')
                return redirect(request.referrer)
            except:
                flash('Error, Please Try Again', 'alert-danger')
                return redirect(request.referrer)
        elif 'it-check' in request.form:
            edit_req = Itcheck.query.filter_by(req_no = dep.id).first()
            access = request.form.get('access')
            internal_email = request.form.get('internal-email')
            external_email = request.form.get('external-email')
            vpn = request.form.get('vpn')
            comment = request.form.get('comment')
            try:
                edit_req.access = req_check(access)
                edit_req.internal_email = req_check(internal_email)
                edit_req.external_email = req_check(external_email)
                edit_req.vpn = req_check(vpn)
                edit_req.comment = comment  
                dep.it_check = edit_req.id
                if dep.facility_check != None or dep.facility_check != '':
                    dep.statue = 'resolved'
                    req.statue = 'resolved'
                db.session.commit()
                flash('Request Updated', 'alert-success')
                return redirect(request.referrer)
            except:
                flash('Error, Please Try Again', 'alert-danger')
                return redirect(request.referrer)
        elif 'close-req' in request.form:
            try:
                cls_req = Requests.query.filter_by(id = request.form['close-req']).first()
                cls_req.statue = 'closed'
                db.session.commit()
                flash('Ticket Closed', 'alert-success')
                return redirect(request.referrer)
            except:
                flash('Error, Please Try Again', 'alert-danger')
                return redirect(request.referrer)
    return render_template("/requests-edit.html", title="Edit Request", req = req, have_pc = have_pc, dep = dep)
    
@req_routes.route("/request/details" , methods=['GET', 'POST'])
@login_required
def requests_details():
    if request.method == 'POST':
        sub_id = request.form['data']

    # ticket_cat = Ticket_cat.query.order_by(id).all()
        ticket_sub_cat = Ticket_subcat.query.filter_by(sub_cat = sub_id).all()
        sub_cat = {}
        for tic in ticket_sub_cat:
            sub_cat[tic.id] = tic.name

    return jsonify(sub_cat)