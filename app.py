from flask import Flask, render_template, request, redirect
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_user, login_required, UserMixin, LoginManager, logout_user


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = 'secret-key'
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    passwd = db.Column(db.String(50))

    def __init__(self, name, email, passwd):
        self.name = name
        self.email = email
        self.passwd = passwd

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', None)
        email = request.form.get('email', None)
        passwd = request.form.get('password', None)
        user = Users(name, email, passwd)

        # User model.save
        db.session.add(user)
        db.session.commit()

        # After user is saved, redirect to private page
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        passwd = request.form.get('password')
        u = Users.query.filter_by(email=email).first()

        if u.passwd == passwd:
            login_user(u)
            return redirect(url_for('private'))
        else:
            return render_template('error_login.html')

    return render_template('login.html')

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/private', methods=['GET'])
@login_required
def private():
    return render_template('private.html')

if __name__ == '__main__':
    app.run()
