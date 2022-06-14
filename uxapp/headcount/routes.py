from flask import Blueprint, redirect, render_template, request, session, url_for, flash, jsonify, current_app
from flask_login import login_required
import os
import pandas as pd 
from uxapp.config import allowed_file
from uxapp.models import  Agents, Leavers
from uxapp import db
import json
from json import JSONEncoder
hc_routes = Blueprint('hc_routes', __name__)
#=========================
# Headcount Route
#=========================
@hc_routes.route("/headcount", methods=['GET', 'POST'])
@login_required
def headcount():
    if request.method == "POST":
        if 'imp-sheet' in request.form:
            upload_file = request.files.get('hcexcel')
            if upload_file and allowed_file(upload_file.filename):
                if upload_file.filename != '':
                    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], upload_file.filename)
                    upload_file.save(file_path)
                    data=pd.read_excel(upload_file)
                    # df = pd.DataFrame(data)#.replace(r'^\s*$', np.nan, regex=True)
                    # duplicated = df[df.duplicated('Biometric')]
                    ckeck = data.values.tolist() #convert excel values into list
                    # print(ckeck)
                    try:
                        for a,b,c,d,e,f in ckeck:   
                            if Agents.query.filter_by(bio = a).all() == []:                    
                                # print(b)
                                # data.to_sql('agents', con = engine, if_exists = 'replace', index = False)
                                add_agent= Agents(bio = a,name = b, l_name = c, start_date = d, depart = str(e), job_title = str(f))
                                db.session.add(add_agent)
                                db.session.commit()
                            else:
                                get_agent = Agents.query.filter_by(bio = a).first()
                                get_agent.bio = a
                                get_agent.name = b
                                get_agent.l_name = c
                                get_agent.start_date = d
                                get_agent.depart = str(e)
                                get_agent.job_title = str(f)
                                db.session.commit()
                        if file_path:
                            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], upload_file.filename))
                    
                        flash('Excel Sheet Imported Successfully', 'alert-success')
                        return redirect(url_for('hc_routes.headcount'))
                    except:
                        flash('Error: Please Try Again ', 'alert-danger')
                        # dubl_json = duplicated.to_json(orient="split")
                        # parsed = json.loads(dubl_json)
                        # print(json.dumps(parsed, indent=4))
                        # for agent in parsed['data']:
                        #     if agent[4] is not None:
                        #         flash( agent[4]  , 'alert-danger')     
                        return redirect(url_for('hc_routes.headcount'))
                else:
                    flash('Faild: Please Import "slsx" Files', 'alert-danger')
                    return redirect(url_for('hc_routes.headcount'))
            else:
                flash('Faild: File extention not valid, Please Import "slsx" Files', 'alert-danger')
                return redirect(url_for('hc_routes.headcount'))     
        elif 'bio' in request.form:
            
            edit_bio = Agents.query.filter_by(id = request.form['id']).first()
            print(edit_bio)
            edit_bio.bio = request.form['bio']
            db.session.commit()
    if 'page' in request.args:
        pageNo = request.args.get('page')
       
    else:
        pageNo = 1
    hc = Agents.query.order_by(Agents.id)
    return render_template("/headcount.html", title="Headcount", headcount = 'active', hc = hc)   
#=========================
# Headcount Update Route
#=========================
@hc_routes.route("/headcount-update", methods=['GET', 'POST'])
@login_required
def headcount_update():
    if request.method == 'POST':
        id = request.form['pk']
        bio = request.form['bio']
        # print(bio)
#=========================
# Leavers Route
#=========================    
@hc_routes.route("/headcount/leavers", methods=['GET', 'POST'])
@login_required
def leavers():
    if request.method == "POST":
        upload_file = request.files.get('lvexcel')
        if upload_file and allowed_file(upload_file.filename):
            if upload_file.filename != '':
                file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], upload_file.filename)
                upload_file.save(file_path)
                xls = pd.ExcelFile(upload_file)
                data=pd.read_excel(xls, 'Leavers')
                # df = pd.DataFrame(data)#.replace(r'^\s*$', np.nan, regex=True)
                # duplicated = df[df.duplicated('Biometric')]
                check = data.values.tolist()
                # print(ckeck)
                try:
                    for a,b,c,d,e,f,g,h,i,j,k in check:
                        if Leavers.query.filter_by(bio = a).all() == []:                    
                            # print(b)
                            # data.to_sql('agents', con = engine, if_exists = 'replace', index = False)
                            add_leave= Leavers(bio = a,name = b, l_name = c, start_date = d,end_date = e, depart = str(g), job_title = str(f), reason = j, sub_reason = k, departure_type = i, manager = h)
                            db.session.add(add_leave)
                            db.session.commit()
                            hc_agent_remove = Agents.query.filter_by(bio = a).first()
                            if hc_agent_remove:
                                db.session.delete(hc_agent_remove)
                                db.session.commit()
                        else:
                            get_agent = Leavers.query.filter_by(bio = a).first()
                            get_agent.bio = a
                            get_agent.name = b
                            get_agent.l_name = c
                            get_agent.start_date = d
                            get_agent.end_date = e
                            get_agent.depart = str(g)
                            get_agent.job_title = str(f)
                            get_agent.reason = j,
                            get_agent.sub_reason = k,
                            get_agent.departure_type = i
                            get_agent.manager = h
                            db.session.commit()
                            # print(int(progress))
                    
                    if file_path:
                        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], upload_file.filename))
                   
                    flash('Excel Sheet Imported Successfully', 'alert-success')
                       
                except:
                    flash('Error: Please Try Again ', 'alert-danger')
                    # dubl_json = duplicated.to_json(orient="split")
                    # parsed = json.loads(dubl_json)
                    # print(json.dumps(parsed, indent=4))
                    # for agent in parsed['data']:
                    #     if agent[4] is not None:
                    #         flash( agent[4]  , 'alert-danger')     
                    return redirect(url_for('hc_routes.leavers'))
            else:
                flash('Faild: Please Import "slsx" Files', 'alert-danger')
                return redirect(url_for('hc_routes.leavers'))
        else:
            flash('Faild: File extention not valid, Please Import "slsx" Files', 'alert-danger')
            return redirect(url_for('hc_routes.leavers'))  
    if 'page' in request.args:
        pageNo = request.args.get('page')
    else:
        pageNo = 1
    class EmployeeEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

    leavers = Leavers.query.order_by(Leavers.id)
    # # result = json.load([i.serialize for i in leavers])
    # # print(result)
    # result =EmployeeEncoder(leavers)
    # return jsonify(leavers = result)
    return render_template('/leavers.html', title = 'Leavers', ac_leavers='active', leavers = leavers)