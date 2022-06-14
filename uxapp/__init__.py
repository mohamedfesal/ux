#=========================
# Import Packages
#=========================
from flask import Flask, render_template,request
# from flask_socketio import SocketIO, send, emit
from flask_mail import Mail
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from numpy import broadcast
from flask_admin import Admin
from uxapp.config import Config


db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
login_manager.login_view ='/'
# socketio = SocketIO()
admin = Admin()
def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    admin.init_app(app)
    db.init_app(app)
    # socketio.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    
    #=============================
    # Init 404 Error Page Handler
    #=============================
    def page_not_found(e):
        return render_template('404.html'), 404
    app.register_error_handler(404, page_not_found)


    #=====================
    # Register Blueprints 
    #=====================
    from uxapp.main.routes import main
    from uxapp.users.routes import users_routes
    from uxapp.pcs.routes import pcs_routes
    from uxapp.wfh.routes import wfh_routes
    from uxapp.headcount.routes import hc_routes
    from uxapp.requests.routes import req_routes
    from uxapp.labels.routes import labels_routes
    from uxapp.stock.routes import stock_routes
    from uxapp.search.routes import search_routes
    from uxapp.todo.routes import todo_routes
    from uxapp.schadul.routes import schadul_routes
    from uxapp.main.global_routes import global_routes
    from uxapp.messages.routes import messages_routes
    from uxapp.Mailer.routes import Mailer
    app.register_blueprint(main)
    app.register_blueprint(users_routes)
    app.register_blueprint(pcs_routes)
    app.register_blueprint(wfh_routes)
    app.register_blueprint(hc_routes)
    app.register_blueprint(req_routes)
    app.register_blueprint(labels_routes)
    app.register_blueprint(stock_routes)
    app.register_blueprint(search_routes)
    app.register_blueprint(todo_routes)
    app.register_blueprint(schadul_routes)
    app.register_blueprint(global_routes)
    app.register_blueprint(messages_routes)
    app.register_blueprint(Mailer)

    return app



