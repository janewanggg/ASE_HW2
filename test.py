from flask_testing import TestCase
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://test_user:asease@localhost/hw2_test'
app.config['TESTING'] = True
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'User'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(45))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

class exampleTest(TestCase):
    TESTING = True
    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost/hw2_test'
        app.config['TESTING'] = True
        return app
    def setUp(self): 
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        all_rows = User.query.all()
        for i in all_rows:
            db.session.delete(i)
        db.session.commit()

    def sign_up(self, username, password):
        #test add new user
        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()
        assert new_user in db.session

    def log_in(self, username, password):
        sign_in_query = User.query.filter_by(username=username, password=password).first()
        return sign_in_query
    
    def modify_password(self, username, password):
        password_query = User.query.filter_by(username=username).first()
        if  password_query is None:
            return password_query
        else:
            password_query.password = password
            db.session.commit()
            return password_query

    def test_cases(self):
        user = User('testUser', '12345')
        db.session.add(user)
        db.session.commit()
        assert user in db.session

        # test user log in sucessfully
        login = self.log_in('testUser','12345')
        assert login is not None

        #test user log in with username not exist
        sign_in_query = self.log_in('tianruip', 'root')
        assert sign_in_query is None

        #test user log in with wrong password not exist
        sign_in_query = self.log_in('root', 'tianruip')
        assert sign_in_query is None

        #test user modify password succesfully
        password_query = self.modify_password('testUser', '123')
        assert password_query is not None
        assert password_query.password == '123'

        #test user modify password but user does not exist
        password_query = self.modify_password('tianruip', '123')
        assert password_query is None
