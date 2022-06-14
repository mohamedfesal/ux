from fileinput import filename
from flask import Blueprint, current_app, redirect, render_template, request, session, url_for, flash, jsonify
from flask_login import login_required, current_user
import datetime
from flask_mail import Message
from uxapp.models import Todolist
from uxapp import db, mail

todo_routes = Blueprint('todo_routes', __name__)

#=========================
# Todo Route
#=========================
@todo_routes.route("/todo" , methods=['GET', 'POST'])
@login_required
def todo():
    if request.method == 'POST':
        todo = request.form['todo_task']
        date_created = datetime.datetime.today()
        added_by = current_user.id
        try:
            add_todo = Todolist(task = todo, date_created = date_created, added_by = added_by, todo_statues = 1 )
            db.session.add(add_todo)
            db.session.commit()
            countTodos = Todolist.query.filter_by(todo_statues = 1).count()
            message = '%s added new task' % current_user.username
            # arquivo = u'downloads/bbbb.txt'
            # attach = u'/uploads/tokens/TMOHAM14_000418596445_41725390.sdtid'
            # with current_app.open_resource("TMOHAM14_000418596445_41725390.sdtid") as fp:
            #     msg.attach("TMOHAM14_000418596445_41725390.sdtid", fp.read())
            subject = "New To Do"
            msg = Message(sender=('UXC App Notifier', 'mohamedfesal99@gmail.com'),
            recipients=['mohamed.faisal@uxcenters.com'],
                    body=message,
                    subject=subject)
            mail.send(msg)
            return jsonify(countTodos)
        except:
            return redirect(request.referrer)
    countTodos = Todolist.query.filter_by(todo_statues = 1).count()
    return jsonify(countTodos)
#=========================    
# Mark Todo Route
#=========================
@todo_routes.route("/mark-todo" , methods=['GET', 'POST'])
@login_required
def markTodo():
    if request.method == 'GET':
        taskId = request.args.get('taskId')
        markTodo = Todolist.query.get_or_404(taskId)
        try:
            markTodo.todo_statues = 0
            db.session.commit() 
            countTodos = Todolist.query.filter_by(todo_statues = 1).count()
            return jsonify(countTodos)
        except:
            return redirect(request.referrer)
    return jsonify({'tasksContent': render_template("/todo.html",target=taskId)})
#=========================    
# Delete Todo Route
#=========================
@todo_routes.route("/delete-todo" , methods=['GET', 'POST'])
@login_required
def deleteTodo():
    if request.method == 'GET':
        taskId = request.args.get('taskId')
        try:
            deleteTodo = Todolist.query.get(taskId)
            db.session.delete(deleteTodo)
            db.session.commit()
            countTodos = Todolist.query.filter_by(todo_statues = 1).count()
            return jsonify(countTodos)
        except:
            return redirect(request.referrer)
    return jsonify({'tasksContent': render_template("/todo.html",target=taskId)})


