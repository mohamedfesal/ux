from flask import Blueprint, redirect, render_template, request, session, url_for, flash, jsonify
from flask_login import login_required
import datetime
from sqlalchemy import desc, extract
from uxapp.models import Users, wfh_pcs, Todolist,pcs

global_routes = Blueprint("global_routes", __name__, url_prefix=None)                               

@global_routes.app_context_processor
def global_var():
    curruent_date = datetime.datetime.today().date()
    # To do Global Var
    todos = Todolist.query.order_by(desc(Todolist.id))
    todosTasksCount = Todolist.query.count()
    todosCount = Todolist.query.filter_by(todo_statues = 1).count()
    # WFH PC Statistics Var
    all_wfh_count = wfh_pcs.query.order_by(wfh_pcs.id).count()
    wfh_out_count = wfh_pcs.query.filter(wfh_pcs.agent !=  None).count()
    wfh_on_count = all_wfh_count - wfh_out_count
    all_pro_pcs = pcs.query.count()
    all_wfh_pcs = wfh_pcs.query.count()
    all_pcs = all_wfh_pcs + all_pro_pcs
    return dict(
        todos = todos,
        todosTasksCount = todosTasksCount,
        todosCount =todosCount,
        all_wfh_count =all_wfh_count,
        wfh_on_count = wfh_on_count,
        wfh_out_count = wfh_out_count,
        all_pcs = all_pcs,
        all_wfh_pcs = all_wfh_pcs,
        all_pro_pcs = all_pro_pcs
        )
