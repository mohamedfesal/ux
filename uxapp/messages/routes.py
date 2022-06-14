from flask import Blueprint, redirect, render_template, request, session, url_for, flash, jsonify, url_for
from flask_login import LoginManager, current_user, login_required
import datetime
from sqlalchemy import desc, extract
from uxapp.models import Users, wfh_pcs, Todolist, Notifications,db
# from flask_socketio import SocketIO, send, emit, join_room
# from uxapp import socketio

messages_routes = Blueprint('messages_routes', __name__)

# users = []

# @messages_routes.route('/messages')
# def index():
#     return render_template('messages.html')


# @socketio.on('connect', namespace='/messages' )
# def connect_handler():
#     if current_user.is_authenticated:
#         if current_user.id not in users:
#             data={'id':current_user.id}
#             users.append(data)
#         emit('connect_res', current_user.id, broadcast=True)
# user = current_user
# @socketio.on('connect', namespace='/notifs')
# def connect_handler():
#     if current_user.is_authenticated:
#         user_room = 'user_{}'.format(session['user_id'])
#         join_room(user_room)
#         emit('response', {'meta': 'WS connected'})
# def create_user_notification(user, action, title, message):
#     """
#     Create a User Notification
#     :param user: User object to send the notification to
#     :param action: Action being performed
#     :param title: The message title
#     :param message: Message
#     """
#     notification = Notifications(user=user,
#                                 action=action,
#                                 title=title,
#                                 body=message,
#                                 received_at=datetime.datetime.today())
#     saved = db.session.commit()

#     if saved:
#         push_user_notification(Users)
# def push_user_notification(current_user):
#     """
#     Push user notification to user socket connection.
#     """
#     user_room = 'user_{}'.format(current_user.id)
#     emit('response',
#          {'meta': 'New notifications',
#           'notif_count': current_user.get_unread_notif_count(),
#           'notifs': Users.get_unread_notifs()},
#          room=user_room,
#          namespace='/notifs')
