from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from cryptography.fernet import Fernet
import json
import os
import hashlib
import secrets
from datetime import datetime
import base64

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Generate a secure secret key

# File paths
PASSWORD_FILE = 'passwords.json'
KEY_FILE = 'key.key'
MASTER_PASSWORD_FILE = 'master_password.hash'

class PasswordManager:
    def __init__(self):
        self.key = self.load_or_generate_key()
        self.cipher = Fernet(self.key)
    
    def load_or_generate_key(self):
        """Load existing key or generate new one"""
        if os.path.exists(KEY_FILE):
            try:
                with open(KEY_FILE, 'rb') as f:
                    key = f.read()
                    # Validate the key
                    if len(key) == 32 and self.is_valid_fernet_key(key):
                        return key
                    else:
                        print("Invalid key found, generating new one...")
                        return self.generate_and_save_key()
            except Exception as e:
                print(f"Error reading key: {e}, generating new one...")
                return self.generate_and_save_key()
        else:
            return self.generate_and_save_key()
    
    def is_valid_fernet_key(self, key):
        """Check if key is valid Fernet key"""
        try:
            Fernet(key)
            return True
        except:
            return False
    
    def generate_and_save_key(self):
        """Generate a new Fernet key and save it"""
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
        print("✅ New encryption key generated and saved")
        return key
    
    def encrypt_password(self, password):
        """Encrypt a password"""
        return self.cipher.encrypt(password.encode()).decode()
    
    def decrypt_password(self, encrypted_password):
        """Decrypt a password"""
        return self.cipher.decrypt(encrypted_password.encode()).decode()
    
    def load_passwords(self):
        """Load all passwords from JSON file"""
        if os.path.exists(PASSWORD_FILE):
            try:
                with open(PASSWORD_FILE, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_passwords(self, passwords):
        """Save passwords to JSON file"""
        with open(PASSWORD_FILE, 'w') as f:
            json.dump(passwords, f, indent=2)
    
    def add_password(self, website, username, password, notes=""):
        """Add a new password entry"""
        passwords = self.load_passwords()
        encrypted_password = self.encrypt_password(password)
        
        entry = {
            'id': secrets.token_hex(8),
            'website': website,
            'username': username,
            'password': encrypted_password,
            'notes': notes,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        passwords.append(entry)
        self.save_passwords(passwords)
        return entry
    
    def get_password(self, entry_id):
        """Get a specific password entry"""
        passwords = self.load_passwords()
        for entry in passwords:
            if entry['id'] == entry_id:
                # Decrypt password before returning
                entry_copy = entry.copy()
                entry_copy['password'] = self.decrypt_password(entry['password'])
                return entry_copy
        return None
    
    def update_password(self, entry_id, website, username, password, notes=""):
        """Update an existing password entry"""
        passwords = self.load_passwords()
        for entry in passwords:
            if entry['id'] == entry_id:
                entry['website'] = website
                entry['username'] = username
                entry['password'] = self.encrypt_password(password)
                entry['notes'] = notes
                entry['updated_at'] = datetime.now().isoformat()
                self.save_passwords(passwords)
                return True
        return False
    
    def delete_password(self, entry_id):
        """Delete a password entry"""
        passwords = self.load_passwords()
        passwords = [entry for entry in passwords if entry['id'] != entry_id]
        self.save_passwords(passwords)
    
    def search_passwords(self, query):
        """Search passwords by website or username"""
        passwords = self.load_passwords()
        query = query.lower()
        results = []
        for entry in passwords:
            if (query in entry['website'].lower() or 
                query in entry['username'].lower()):
                entry_copy = entry.copy()
                entry_copy['password'] = self.decrypt_password(entry['password'])
                results.append(entry_copy)
        return results

# Password manager instance
pm = PasswordManager()

# Master password functions
def set_master_password(password):
    """Set master password hash"""
    salt = secrets.token_hex(32)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    with open(MASTER_PASSWORD_FILE, 'w') as f:
        json.dump({'hash': password_hash, 'salt': salt}, f)

def verify_master_password(password):
    """Verify master password"""
    if not os.path.exists(MASTER_PASSWORD_FILE):
        return False
    
    with open(MASTER_PASSWORD_FILE, 'r') as f:
        data = json.load(f)
    
    password_hash = hashlib.sha256((password + data['salt']).encode()).hexdigest()
    return password_hash == data['hash']

# Routes
@app.route('/')
def index():
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        
        # First time setup
        if not os.path.exists(MASTER_PASSWORD_FILE):
            set_master_password(password)
            session['authenticated'] = True
            flash('Master password set successfully!', 'success')
            return redirect(url_for('dashboard'))
        
        # Verify master password
        if verify_master_password(password):
            session['authenticated'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid master password!', 'error')
    
    return render_template('login.html', first_time=not os.path.exists(MASTER_PASSWORD_FILE))

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    passwords = pm.load_passwords()
    # Decrypt passwords for display
    for entry in passwords:
        entry['display_password'] = '•' * 12  # Show dots for security
    
    return render_template('dashboard.html', passwords=passwords)

@app.route('/add_password', methods=['POST'])
def add_password():
    if 'authenticated' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        website = request.form['website']
        username = request.form['username']
        password = request.form['password']
        notes = request.form.get('notes', '')
        
        if not all([website, username, password]):
            return jsonify({'error': 'Please fill all required fields'}), 400
        
        entry = pm.add_password(website, username, password, notes)
        flash('Password added successfully!', 'success')
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_password/<entry_id>')
def get_password(entry_id):
    if 'authenticated' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    entry = pm.get_password(entry_id)
    if entry:
        return jsonify(entry)
    return jsonify({'error': 'Password not found'}), 404

@app.route('/update_password', methods=['POST'])
def update_password():
    if 'authenticated' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        entry_id = request.form['entry_id']
        website = request.form['website']
        username = request.form['username']
        password = request.form['password']
        notes = request.form.get('notes', '')
        
        if pm.update_password(entry_id, website, username, password, notes):
            flash('Password updated successfully!', 'success')
            return jsonify({'success': True})
        return jsonify({'error': 'Password not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_password/<entry_id>', methods=['POST'])
def delete_password(entry_id):
    if 'authenticated' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    pm.delete_password(entry_id)
    flash('Password deleted successfully!', 'success')
    return jsonify({'success': True})

@app.route('/search_passwords')
def search_passwords():
    if 'authenticated' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    query = request.args.get('q', '')
    if query:
        results = pm.search_passwords(query)
        return jsonify(results)
    return jsonify([])

@app.route('/generate_password')
def generate_password():
    """Generate a random secure password"""
    import string
    
    length = 16
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(chars) for _ in range(length))
    return jsonify({'password': password})

if __name__ == '__main__':
    app.run(debug=True)