from flask import Blueprint, redirect, render_template, request, session, url_for, flash, jsonify
from flask_login import login_required
from uxapp.models import Leaves

schadul_routes = Blueprint('scadul_routes', __name__)

@schadul_routes.route('/schadul', methods=['GET', 'POST'])
@login_required
def schadul():
    leaves = Leaves.query.all()
    return render_template('/schadul.html', title="Schadul", schadul="active", leaves = leaves)