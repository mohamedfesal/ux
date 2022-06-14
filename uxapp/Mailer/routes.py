from fileinput import filename
from turtle import title
from flask import Blueprint, render_template, request, flash,current_app, url_for
from flask_login import login_required
from uxapp.models import  Department, Users, wfh_pcs, pcs
from flask_mail import Message
from uxapp import db, mail
import os
from os.path import join, dirname, realpath

Mailer = Blueprint('Mailer', __name__)

@Mailer.route('/mailer', methods=['GET','POST'])
@login_required
def mailer():
	if request.method == "POST":
		tl = request.form['tl-team']
		tl_mail = Users.query.filter(Users.id == tl).first()
		team = wfh_pcs.query.filter(wfh_pcs.tl == tl).all()
		
		message = render_template('mailer/mail-template.html', team = team, tl = tl_mail)
		subject = "WFH Tokens"
		cc = ['mohamed.faisal@uxcenters.com']
		msg = Message(sender=('UXC App Notifier - no-reply ', 'it-support-alex@uxcenters.com'),
		recipients=[tl_mail.email],
				html=message,
				subject=subject, cc = cc)
		
		for agent in team:
			# print(agent)
			for fname in os.listdir(current_app.config["UPLOAD_RSA_FOLDER"]):
				sp = fname.split("_")
				# print(len(sp))
				if len(sp) == 3:
					global bio
					bio = sp[2].split(".")[0]
					# print(agent.agentpc.bio)
					# print(bio)
				if str(agent.agentpc.bio) == str(bio.strip()):
					with current_app.open_resource(current_app.config["UPLOAD_RSA_FOLDER"] + '/' + fname) as fp:
						msg.attach(fname,"DLL/EXE", fp.read())
					print(fname)
		mail.send(msg)
	tls = Users.query.join(Department).filter(Department.dep_name == 'TL')
	return render_template('mailer/wfh-mail.html', title = 'WFH Mailer', tls = tls)