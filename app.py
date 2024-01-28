from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'
db = SQLAlchemy(app)

#################### MODELS ####################
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    
class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participants = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    messages = db.relationship('Message', backref='conversation', lazy=True)

    def __repr__(self):
        return '<Conversation %r>' % self.id

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80), nullable=False)
    receiver = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)

    def __repr__(self):
        return '<Message %r>' % self.text

#################### ROUTES ####################

@app.route('/')
def index():
    redirect('/login')

@app.route('/login') 
def login():
    if()
    return render_template('login.html')

@app.route("/dashboard")

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)