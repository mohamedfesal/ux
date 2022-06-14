from flask import Blueprint, render_template, request, flash
from flask_login import login_required
from uxapp.models import  wfh_pcs, pcs

labels_routes = Blueprint('labels_routes', __name__)

#=========================
# Print Labels Route
#=========================
@labels_routes.route("/labels" , methods=['GET', 'POST'])
@login_required
def labels():
    floor_cat = []
    if request.method == 'POST':
        pcs_range = request.form['pcs-range']
        label_option = request.form['label-option']
        if 'floor' in request.form:
            floor = request.form['floor']
        pclist = pcs_range.split(',')
        def get_label(pc):
                pc= int(pc)
                if label_option == 'wfh':
                    pcs_query = wfh_pcs.query.filter_by(station = pc).first()
                elif label_option == 'pro':
                    pcs_query = pcs.query.filter_by(station = pc, floor = floor).first()
                # print(pcs_query)
                elif label_option == '':
                    flash('Please Select Station Type', 'alert-danger')
                if pcs_query != None: 
                    return pcs_query
                else:
                    return None
        return render_template("/label-print.html", title="label Print", pclist = pclist, label =get_label, floor_cat = floor_cat)
    pc_floor = pcs.query.order_by(pcs.id)
    for floor in pc_floor:
        if floor.floor not in floor_cat:
            floor_cat.append(floor.floor)
    # print(floor_cat)
    return render_template("/label-print.html", title="label Print",pr_lable = 'active', floor_cat = floor_cat)