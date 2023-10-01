from flask import Flask, render_template, request, redirect, url_for, session
from pyrebase import pyrebase
import os
from google.cloud import firestore

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure Firebase
firebase_config = {
    # Fill in your Firebase configuration details
}
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firestore.Client()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = auth.create_user_with_email_and_password(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

# ... (Previous code)

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user_token' in session:
        user_token = session['user_token']
        user = auth.get_account_info(user_token)
        user_id = user['users'][0]['localId']
        message_text = request.form['message']
        db.collection('messages').add({
            'user_id': user_id,
            'message_text': message_text,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        return redirect(url_for('messages'))
    return redirect(url_for('login'))

@app.route('/messages')
def messages():
    if 'user_token' in session:
        user_token = session['user_token']
        user = auth.get_account_info(user_token)
        user_id = user['users'][0]['localId']
        messages = db.collection('messages').where('user_id', '==', user_id).order_by('timestamp').stream()
        return render_template('messages.html', messages=messages)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
