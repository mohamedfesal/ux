from flask import Blueprint, redirect, render_template, request, session, url_for, flash, jsonify, send_file
from flask_login import login_required
import os
import json
import pandas as pd 
from uxapp.config import engine, allowed_file
from uxapp.models import pcs
from uxapp import db

pcs_routes = Blueprint('pcs_routes', __name__)
#=========================
# PCs Details Route
#=========================
@pcs_routes.route("/pcdetails" , methods=['GET', 'POST'])
@login_required
def pcdetails():
    if request.method == "POST":
        if 'addpc' in request.form:
            site = request.form['site']
            build = request.form['build']
            floor = request.form['floor']
            pc_no = request.form['pc_no']
            pc_host = request.form['pc_host']
            ip = request.form['pc_ip']
            pbxuser = request.form['pbxuser']
            ciscodid = request.form['ciscodid']
            
            Pc= pcs.query.filter_by(id = pc_no).first()
            PC_name = pcs.query.filter_by(hostname = pc_host).first()
            if Pc is None:
                if pcs.query.filter_by(hostname = pc_host).first() is None:
                    Pc = pcs(site = site, build = build, floor = floor, station = pc_no, hostname = pc_host,ip = ip, pbxuser = pbxuser, ciscodid = ciscodid)
                    db.session.add(Pc)
                    db.session.commit()
                    return jsonify({'success':'PC Added Successfuly'})
                    flash('PC Added Successfuly', 'alert-success')
                else:    
                    flash('PC Is Already Exist In Table','alert-danger')  
                    return jsonify({'error':'PC Is Already Exist In Table'}) 
            else:    
                return jsonify({'error':'PC Is Already Exist In Table'}) 
                flash('PC Is Already Exist In Table', 'alert-danger')   
        elif 'editpc' in request.form:
            e_id = request.form['pc-id']
            e_site = request.form['site']
            e_build = request.form['build']
            e_floor = request.form['floor']
            e_station = request.form['station']
            e_hostname = request.form['hostname']
            e_ip = request.form['ip']
            e_bpxuser = request.form['pbxuser']
            e_ciscodid = request.form['ciscodid']
            try:
                pc = pcs.query.filter_by(id = e_id).first()
                pc.site = e_site
                pc.build = e_build
                pc.floor = e_floor
                pc.station = e_station
                pc.hostname = e_hostname
                pc.ip = e_ip
                pc.pbxuser = e_bpxuser
                pc.ciscodid = e_ciscodid
                db.session.commit()
                flash('PC Updated Successfully', 'alert-success')
                return redirect(url_for('pcs_routes.pcdetails'))
            except:
                flash('Error, Please Try Again', 'alert-danger')
                return redirect(url_for('pcs_routes.pcdetails'))
    pcs_table =  pcs.query.order_by(pcs.id) 
    return render_template("/pcdetails.html", title="PCs Details", pcdetails="active", pcs_table = pcs_table)
#====================================
# PCS Pagination Route
#====================================    
@pcs_routes.route("/pcdetails/<int:page_num>" , methods=['GET', 'POST'])
@login_required
def pcpagin(page_num):
    pcs_table = pcs.query.order_by(pcs.id) 
    return render_template("/pcdetails.html", title="PCs Details", pcdetails="active", pcs_table = pcs_table, page_num = page_num)    
#====================================
# Import PCs from Excel Sheet  Route
#====================================
@pcs_routes.route("/upload-pcs" , methods=['GET', 'POST'])
@login_required
def uploadpcs():
    if request.method == "POST":
        upload_file = request.files.get('pcexc')
        if upload_file and allowed_file(upload_file.filename):
            if upload_file.filename != '':
                file_path = os.path.join(pcs_routes.config["UPLOAD_FOLDER"], upload_file.filename)
                upload_file.save(file_path)
                data=pd.read_excel(upload_file)
                df = pd.DataFrame(data)
                duplicated = df[df.duplicated('HOSTNAME')]
                ckeck = data.values.tolist()
                for a,b,c,d,e,f,g,h in ckeck:
                    try:
                        if pcs.query.filter_by(hostname = e).all() != [] and pcs.query.filter_by(pbxuser = g).all() != [] and pcs.query.filter_by(ciscodid = h).all() != []:
                            flash('There is Dublicated Hostname > '+ e, 'alert-danger')
                            flash('There is Dublicated DID User > '+ str(g).rsplit('.', -1)[-1], 'alert-danger')
                            flash('There is Dublicated DID Extention > '+ str(h).rsplit('.', -1)[-1], 'alert-danger')
                        else:
                            data.to_sql('pcs', con = engine, if_exists = 'append', index = False)
                            flash('Excel Sheet Imported Successfully', 'alert-success')
                            return redirect(url_for('pcs_routes.pcdetails'))
                    except:
                        flash('Error: There is Dublicated Items In your Excel Sheet or Column Names incorrect ', 'alert-danger')
                        dubl_json = duplicated.to_json(orient="split")
                        parsed = json.loads(dubl_json)
                        # print(json.dumps(parsed, indent=4))
                        for pc in parsed['data']:
                            if pc[4] is not None:
                                flash( pc[4]  , 'alert-danger')                        
                        return redirect(url_for('pcs_routes.pcdetails'))
            else:
                flash('Faild: Please Import "slsx" Files', 'alert-danger')
        else:
            flash('Faild: File extention not valid, Please Import "slsx" Files', 'alert-danger')
            return redirect(url_for('pcs_routes.pcdetails'))         
        
        return redirect(url_for('pcs_routes.pcdetails'))
#=====================================
# Export PCs from Excel Sheet  Route
#=====================================
@pcs_routes.route("/export-pcs" , methods=['GET', 'POST'])
@login_required
def exportpcs():
        pcs_table = pd.read_sql_query('SELECT site, build,floor,station,hostname, ip, pbxuser, ciscodid FROM pcs', engine)
        df1 = pd.DataFrame(pcs_table)
        # writing to Excel
        df1.to_excel("static/download/HostNames Inventory.xlsx", sheet_name='Alex')
        file_path = 'static/download/HostNames Inventory.xlsx'
        download = send_file(file_path, as_attachment=True)
        return download 
#=========================        
# Edit Pc Route
#=========================
@pcs_routes.route("/edit-pc" , methods=['GET', 'POST'])
@login_required
def edit_pc():
    return render_template("/edit-pc.html", title="Edit PC")