from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sys
import os

sys.path.insert(0, '/d3b4/usr/workdir')
from auth_module import verify_login, get_credentials, update_credentials, get_settings, update_settings

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if verify_login(username, password):
            session['logged_in'] = True
            session['username'] = username
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'})
    
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return jsonify({'success': True})

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/api/settings', methods=['GET', 'POST'])
def api_settings():
    if 'logged_in' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if request.method == 'GET':
        settings = get_settings()
        return jsonify(settings)
    
    elif request.method == 'POST':
        data = request.get_json()
        if update_settings(data):
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Failed to update settings'})

@app.route('/api/credentials', methods=['POST'])
def api_credentials():
    if 'logged_in' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if update_credentials(username, password):
        session['username'] = username
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Failed to update credentials'})

@app.route('/api/current_user', methods=['GET'])
def current_user():
    if 'logged_in' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    creds = get_credentials()
    return jsonify({
        'username': creds['username'] if creds else session.get('username'),
        'settings': get_settings()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
