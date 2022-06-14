from flask import Blueprint, redirect, render_template, request, session, url_for, flash, jsonify
from flask_login import login_required
from sqlalchemy import or_
from uxapp.models import  wfh_pcs, Agents, pcs

search_routes = Blueprint('search_routes', __name__)
#=========================
# Seach Results Route
#========================= 
@search_routes.route("/search" , methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        try:
            search = request.args.get('search')
            query = request.form['query']
            # print(query)
            tag = '%{}%'.format(query)
            tags = '%{}%'.format(search)
            ref = request.referrer.split('/')[-1]
            if request.referrer.split('/')[-1] == url_for('pcs_routes.pcdetails').split('/')[-1]: 
                results = pcs.query.filter(or_(pcs.hostname.like(tags) , pcs.station.like(tags))).all()
            elif request.referrer.split('/')[-1] == url_for('wfh_routes.wfhpcs').split('/')[-1] or request.referrer.split('/')[-1] == url_for('wfh_routes.wfhtracker').split('/')[-1]:
                if search.isdigit() == True:
                    ag = Agents.query.filter(Agents.bio.like(tags)).first()
                    agid = ag.id
                else:
                    agid = 0
                results = wfh_pcs.query.filter(or_(wfh_pcs.hostname.like(tags) , wfh_pcs.station.like(tags), wfh_pcs.agent.like(agid))).all()
            elif request.referrer.split('/')[-1] == url_for('hc_routes.headcount').split('/')[-1]:
                if query != '':
                    hc_results = Agents.query.filter(or_(Agents.bio.like(tag) , (Agents.name + ' ' + Agents.l_name).like(tag))).all()
                return jsonify({'headcounts': render_template("/headcount-search.html", hc_results = hc_results, ref = ref)})
                # return render_template("/search.html", title="Seach Results", hc_results = hc_results, ref = ref)
            if results:
                return render_template("/search.html", title="Seach Results", results = results, ref = ref)
            else:
                flash("Search Results Not Found, Try With Different Keyword", 'alert-danger')
                return render_template("/search.html", title="Seach Results")
        except:
            flash("Error, Please Try Again", 'alert-danger')
    return render_template("/search.html", title="Seach Results")
