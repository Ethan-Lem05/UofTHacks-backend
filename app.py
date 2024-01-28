from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'test.db')
db = SQLAlchemy(app)
SocketIO = SocketIO(app)
live_connections = {}

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
    sender = db.Column(db.Integer, nullable=False)
    receiver = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    received = db.Column(db.Boolean, nullable=False)
    conversation_id = db.Column(db.ForeignKey('conversation.id'), nullable=False)

    def __repr__(self):
        return '<Message %r>' % self.text

#################### ROUTES ####################

@app.route('/')
def index():
    return redirect('/login', 302)

@app.route('/login', methods=['GET', 'POST']) 
def login():
    if(request.method == 'POST'):  
        session['username'] = request.form['username']
        return redirect(url_for('dashboard')),200
    else:
        return render_template('login.html'), 200

@app.route("/dashboard")
def dashboard():
    return (render_template("Dashboard.html"), 200)

################# FETCH POINTS ##################

@app.route("/recap")
def recap():
    
    recap_dict = []
    return jsonify(recap_dict), 200

#################### SOCKETS ####################

@SocketIO.on('connect')
def handle_connect():
    id = session[id]
    live_connections[id] = request.sid

@SocketIO.on('json')
def handle_message(msg):
    message = {
            'sender': msg.sender,
            'receiver': msg.receiver,
            'text': msg.text,
            'created_at': msg.created_at,
            'received': False,
            'conversation_id': msg.conversation_id
        }
    if message.receiver in live_connections:
        message.received = True
        SocketIO.emit('json', msg, room=live_connections[msg.receiver])
    else:
        db.session.add(message)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    SocketIO.run(app, debug=True)