from flask import Flask, render_template, request, redirect
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Users(db.Model):
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

        return redirect(url_for('login'))

        
        # After user is saved, redirect to private page
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        passwd = request.form.get('password')
        u = Users.query.filter_by(email=email).first()

        if u.passwd == passwd:
            return redirect(url_for('private'))

    return render_template('login.html')

@app.route('/private')
def private():
    return render_template('private.html')

if __name__ == '__main__':
    app.run()
