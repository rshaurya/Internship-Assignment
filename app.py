from flask import Flask, render_template, request, redirect
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        return redirect(url_for('login'))

        # User model.save
        # After user is saved, redirect to private page
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/private')
def private():
    return render_template('/private.html')


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    passwd = db.Column(db.String(50))

if __name__ == '__main__':
    app.run(debug=True)
