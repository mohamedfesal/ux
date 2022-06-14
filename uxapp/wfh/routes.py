from distutils.command.upload import upload
from fileinput import filename
from flask import Blueprint, redirect, render_template, request, session, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
import datetime
from uxapp.models import wfh_pcs, Agents, Returned, Users, Department
from uxapp import db
from uxapp.config import allowed_rsa_file, allowed_file
import pandas as pd 
import os
wfh_routes = Blueprint('wfh_routes', __name__)
#=========================
# Tracker Route
#=========================
@wfh_routes.route("/wfhtracker" , methods=['GET', 'POST'])
@login_required
def wfhtracker():
    if request.method == "POST":
        if 'add-wfh' in request.form:
            # Get "Add Agent to PC" inputs
            pc_no = request.form['pc_no']
            agentBio = request.form['agentbio']
            agentTl = request.form['agent-tl']
            # upload_file = request.files['rsa-file']
            # print(upload_file)
            wfhpc= wfh_pcs.query.filter_by(station = pc_no).first()
            pc_check = wfh_pcs.query.filter_by(station = pc_no).first()
            # print(pc_check)
            if not pc_check:
                # return jsonify({'error':'PC is Not Exist'})
                flash('PC is Not Exist', 'alert-danger')
            elif wfhpc.agent is not None:
                # return jsonify({'error':'PC is Already have Agent, Kindly remove Agent first or Move it to Returned PCs'})
                flash('PC is Already Taken, Kindly remove Agent first or Move it to Returned PCs', 'alert-danger')
            elif wfhpc is not None:
                get_agent = Agents.query.filter_by(bio = agentBio).first()
                # if get_agent != None:
                #     # Add agent ID to foreignKey column
                #     wfhpc.agent = get_agent.id
                #     wfhpc.wfhdate = datetime.datetime.today()
                #     wfhpc.dlv_by = current_user.username
                #     db.session.commit()
                #     return jsonify({'success':'PC Added Successfuly'})
                #     flash('PC Added Successfuly', 'alert-success')

                if wfhpc.agent != None: # Check if pc have agent
                    # return jsonify({'error':'PC is Already have Agent'})
                    flash('PC is Already have Agent', 'alert-danger')
                    return redirect(url_for('wfh_routes.wfhtracker'))
                else:
                    if get_agent is not None: # Check if Agent Exist in Headcount
                        get_agent_count = wfh_pcs.query.filter_by(agent = get_agent.id).count() #check if agent have pc
                        if get_agent_count >= 1:
                            # return jsonify({'error':'Agent is Already have PC'})
                            flash('Agent already have a PC', 'alert-danger')
                        else: 
                            # if upload_file and allowed_rsa_file(upload_file.filename):
                            #     if upload_file.filename != '':
                            #         file_path = os.path.join(current_app.config["UPLOAD_RSA_FOLDER"], upload_file.filename)
                            #         upload_file.save(file_path)
                            wfhpc.agent = get_agent.id
                            wfhpc.wfhdate = datetime.datetime.today()
                            wfhpc.dlv_by = current_user.username
                            wfhpc.tl = agentTl
                            # wfhpc.token = url_for('static', filename = "uploads/tokens/" + upload_file.filename)
                            db.session.commit()
                            # return jsonify({'success':'Agent Added To PC Successfuly'})
                            flash('Agent has been Updated', 'alert-success')
                            return redirect(url_for('wfh_routes.wfhtracker'))
                        # else:
                        #     flash('Please Select RSA Token for the agent', 'alert-danger')
                        #     return redirect(url_for('wfh_routes.wfhtracker'))
                        #     # return jsonify({'Error':'Please Select RSA Token for the agent'})
                        #     else:
                        #         flash('RSA File Extention is Not Valid', 'alert-danger')
                        #         return redirect(url_for('wfh_routes.wfhtracker'))
                        #         # return jsonify({'Error':'RSA File Extention is Not Valid'})
                    else:
                        # return jsonify({'error':'Agent Not Exist In Headcount!'})
                        flash('Agent not exist in headcount', 'alert-danger') 
                        return redirect(url_for('wfh_routes.wfhtracker'))
            else:    
            # return jsonify({'error':'Error, Please Try again!'})
                flash('Error, Please Try again!', 'alert-danger') 
                return redirect(url_for('wfh_routes.wfhtracker'))
        elif 'upload-sheet' in request.form :
             file = request.files.get('sheet')
             if file and allowed_file(file.filename):
                if file.filename != '':
                    read_data = pd.read_excel(file)
                    data = read_data.fillna('')
                    excel_values = data.values.tolist()
                    for value in excel_values:
                        wfhpc= wfh_pcs.query.filter_by(station = value[0]).first()
                        get_agent = Agents.query.filter_by(bio = value[1]).first()
                        tl = Users.query.filter_by(bio = value[5]).first()
                        if wfhpc.agent != None: # Check if pc have agent
                            flash('PC is Already have Agent', 'alert-danger')
                        else:
                            if get_agent is not None: # Check if Agent Exist in Headcount
                                get_agent_count = wfh_pcs.query.filter_by(agent = get_agent.id).count() #check if agent have pc
                                if get_agent_count >= 1:
                                    flash('Agent already have a PC', 'alert-danger')
                                else: 
                                    wfhpc.agent = get_agent.id
                                    # wfhpc.wfhdate = datetime.datetime.today()
                                    if tl != None:
                                        wfhpc.tl = tl.id
                                    db.session.commit()
                            else:
                                flash('Agent not exist in headcount', 'alert-danger') 
                    else:    
                        flash('Error, Please Try again!', 'alert-danger') 
                flash('Sheet has been imported', 'alert-success')
        elif 'delete-selected' in request.form:
            pcs_id = request.form['delete-selected']
         
            pcs_list = pcs_id.split(',')
            print(pcs_id)
            try:
                for pc in pcs_list:
                    print(pc)
                    wfhdelete = wfh_pcs.query.filter_by(id = pc).first()
                    # print(wfhdelete)
                    wfhdelete.agent = None
                    wfhdelete.wfhdate = None
                    wfhdelete.dlv_by = None
                    db.session.commit()
                flash('Agents Deleted From WFH Tracker Successfuly', 'alert-success') 
                # return render_template("/wfhtracker.html", title="Edit WFH Item", wfhdelete=wfhdelete)
            except Exception as e:
                flash('Error: Please Try again', 'alert-danger')
                flash('Error:' + str(e), 'alert-danger')
                return redirect(url_for('wfh_routes.wfhtracker'))
    # Query To Filter WFH PCs Tabel
    wfh_table = wfh_pcs.query.filter(wfh_pcs.agent !=  None)
    returned_table = Returned.query.order_by(Returned.id)
    tls = Users.query.join(Department).filter(Department.dep_name == 'TL').all()
    return render_template("/wfhtracker.html", title="Tracker", wfhtracker="active", wfh_table = wfh_table, returned_table = returned_table, tls= tls) 
#=========================
# Delete WFH PC Route
#=========================
@wfh_routes.route("/delete-wfh/<int:id>" , methods=['GET', 'POST'])
@login_required
def deletewfh(id):
    wfhdelete = wfh_pcs.query.get_or_404(id)
    try:
        wfhdelete.agent = None
        wfhdelete.wfhdate = None
        wfhdelete.dlv_by = None
        db.session.commit()
        flash('Agent Deleted From WFH Tracker Successfuly', 'alert-success') 
        return redirect(url_for('wfh_routes.wfhtracker'))
        # return render_template("/wfhtracker.html", title="Edit WFH Item", wfhdelete=wfhdelete)
    except:
        flash('Error: Please Try again', 'alert-danger')
        return redirect(url_for('wfh_routes.wfhtracker'))

#=============================
# Move To Returned PCs Route
#=============================
@wfh_routes.route("/move-returned-wfh/" , methods=['GET', 'POST'])
@login_required
def returned():
    if request.method == "POST":
        # Get Returned PC inputs
        returned_pc = request.form['rd-pc-no']
        rd_pc_statue = request.form['rd-pc-statue']
        rd_screens_statue = request.form['rd-screens-statue']
        rd_headset_statue = request.form['rd-headset-statue']
        rd_hdd_statue = request.form['rd-hdd-statue']
        rd_comment = request.form['rd-comment']  
        returned_pc_no = wfh_pcs.query.filter_by(id = returned_pc).first()
        if returned_pc_no is not None:
            returned_pc_no = Returned(r_agent = returned_pc_no.agentpc.name, r_agent_bio = returned_pc_no.agentpc.bio, r_pc = returned_pc_no.hostname, pc_statue = rd_pc_statue, hdd_statue = rd_hdd_statue, screens_statue = rd_screens_statue, headset_statue = rd_headset_statue,r_date = datetime.datetime.today(), ckecked_by = current_user.username, comment = rd_comment)
            db.session.add(returned_pc_no)
            db.session.commit()
            wfh_pcs.query.filter_by(id = returned_pc).first().agent = None
            wfh_pcs.query.filter_by(id = returned_pc).first().wfhdate = None
            wfh_pcs.query.filter_by(id = returned_pc).first().dlv_by = None
            db.session.commit()
            flash('Agent Moved To Returned WFH PCs Successfuly', 'alert-success') 
            return redirect(url_for('wfh_routes.wfhtracker'))
        else:
            flash('Error: Please Try again', 'alert-danger')
            return redirect(url_for('wfh_routes.wfhtracker'))
    else:
        return redirect(url_for('wfh_routes.wfhtracker'))
#=========================
# WFH PCs Route
#=========================
@wfh_routes.route("/wfh-pcs" , methods=['GET', 'POST'])
@login_required
def wfhpcs():
    if request.method == "POST":
        if 'addpc' in request.form:
            pc_no = request.form['pc_no']
            pc_host = request.form['pc_host']
            pbxuser = request.form['pbxuser']
            ciscodid = request.form['ciscodid']
            # print('True')
            Pc= wfh_pcs.query.filter_by(station = pc_no).first()
            if Pc is None:
                if wfh_pcs.query.filter_by(hostname = pc_host).first() is None:
                    Pc = wfh_pcs(station = pc_no, hostname = pc_host, pbxuser = pbxuser, ciscodid = ciscodid)
                    db.session.add(Pc)
                    db.session.commit()
                    # return jsonify({'success':'PC Added Successfuly'})
                    flash('PC Added Successfuly', 'alert-success')
                    return redirect (url_for('wfh_routes.wfhpcs'))
                else:    
                    flash('PC Is Already Exist In Table','alert-danger')  
                    return redirect (url_for('wfh_routes.wfhpcs'))
                    # return jsonify({'error':'PC Is Already Exist In Table'}) 
            else:    
                # return jsonify({'error':'PC Is Already Exist In Table'}) 
                flash('PC Is Already Exist In Table', 'alert-danger')  
                return redirect (url_for('wfh_routes.wfhpcs'))
        elif 'editpc' in request.form:
            e_id = request.form['pc-id']
            # e_site = request.form['site']
            # e_build = request.form['build']
            # e_floor = request.form['floor']
            e_station = request.form['station']
            e_hostname = request.form['hostname']
            # e_ip = request.form['ip']
            e_bpxuser = request.form['pbxuser']
            e_ciscodid = request.form['ciscodid']
            try:
                pc = wfh_pcs.query.filter_by(id = e_id).first()
                # pc.site = e_site
                # pc.build = e_build
                # pc.floor = e_floor
                pc.station = e_station
                pc.hostname = e_hostname
                # pc.ip = e_ip
                pc.pbxuser = e_bpxuser
                pc.ciscodid = e_ciscodid
                db.session.commit()
                flash('PC Updated Successfully', 'alert-success')
                return redirect(url_for('wfh_routes.wfhpcs'))
            except:
                flash('Error, Please Try Again', 'alert-danger')
                return redirect(url_for('wfh_routes.wfhpcs'))
        elif 'upload-sheet' in request.form:
            file = request.files.get('sheet')
            if file and allowed_file(file.filename):
                if file.filename != '':
                    read_data = pd.read_excel(file)
                    data = read_data.fillna('')
                    excel_values = data.values.tolist()
                    #pcs = wfh_pcs.query
                    # print(read_data)
                    for record in excel_values:
                        # print(record[0])
                        add_wfh_pc = wfh_pcs(station = record[0], hostname = record[3], pbxuser = record[4] )
                        db.session.add(add_wfh_pc)
                        db.session.commit()
                    flash('File Imported Succsessfully', 'alert-success')
                
    pcs_table = wfh_pcs.query.order_by(wfh_pcs.hostname)   
    return render_template("/wfhpcs.html", title="WFH PCs", wfhpcs="active", pcs_table = pcs_table)