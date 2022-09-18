from flask_cors import *
from flask_sqlalchemy import SQLAlchemy

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import hashlib
from flask import Flask


class Config:
    def __init__(self):
        self.app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')
        self.db = SQLAlchemy(self.app)

    def create_app(self):
        DIALECT = 'mysql'
        DRIVER = 'pymysql'
        USERNAME = 'root'
        PASSWORD = 'Michael4011'
        HOST = '127.0.0.1'
        PORT = '3306'
        DATABASE = 'student'
        self.app.config['SQLALCHEMY_DATABASE_URI'] = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
            DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
        )
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
        self.app.config['SESSION_TYPE'] = 'sqlalchemy'  # session type is sqlalchemy
        self.app.config['SESSION_SQLALCHEMY'] = self.db  # SQLAlchemy Object
        self.app.config['SESSION_SQLALCHEMY_TABLE'] = 'session'  # session to store the table name
        self.app.config['SESSION_PERMANENT'] = True  # If set to True，session will lose when the browser closed.
        self.app.config['SESSION_USE_SIGNER'] = True
        self.app.config['SESSION_KEY_PREFIX'] = 'session:'
        self.app.config['MAIL_DEBUG'] = True  # open debug, easy for maintain
        self.app.config['MAIL_SUPPRESS_SEND'] = False  # send email, if ture, not send
        self.app.config['MAIL_SERVER'] = 'smtp.qq.com'  # mail server
        self.app.config['MAIL_PORT'] = 465  # mail port number
        self.app.config['MAIL_USE_SSL'] = True
        self.app.config['MAIL_USE_TLS'] = False
        self.app.config['MAIL_USERNAME'] = '905528647@qq.com'  # email address
        self.app.config['MAIL_PASSWORD'] = 'twskmrgecbwgbffd'  # email password
        self.app.config['MAIL_DEFAULT_SENDER'] = '905528647@qq.com'  # email address，default sender
        # Celery configuration
        self.app.config['CELERY_BROKER_URL'] = 'redis://@localhost:6379/1'
        self.app.config['CELERY_RESULT_BACKEND'] = 'redis://@localhost:6379/2'
        self.app.config['VUE_PORT'] = 8081
        self.migrate = Migrate(self.app, self.db)
        self.manager = Manager(self.app)
        self.manager.add_command('db', MigrateCommand)
        CORS(self.app, supports_credentials=True)
        self.app.jinja_env.variable_start_string = '{['
        self.app.jinja_env.variable_end_string = ']}'
        self.app.secret_key = hashlib.sha1('abcdefg'.encode()).hexdigest()
        return self.app

    def get_db(self):
        return self.db

    def init_session(self):
        self.db.create_all()




config = Config()

from flask_mail import Mail, Message
from celery import Celery

app = config.create_app()
mail = Mail(app)
# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def send_async_email(email_data):
    """Background task to send an email with Flask-Mail."""
    msg = Message(email_data['subject'],
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
    msg.html = email_data['body']
    with app.app_context():
        mail.send(msg)

