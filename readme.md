# 🔐 Simple Personal Password Manager

A secure, easy-to-use personal password manager built with Python Flask. Store and manage your passwords with military-grade encryption in a simple web interface.

![Password Manager Demo]([https://via.placeholder.com/800x400/0d6efd/ffffff?text=Simple+Password+Manager](https://github.com/Digitalspy12/Personal-Password-Manager-/blob/main/account-recovery.png))

## ✨ Features

- 🔒 **Military-grade encryption** using Fernet (AES-128 + HMAC)
- 🔑 **Master password protection** for accessing your vault
- 🌐 **Responsive web interface** that works on desktop and mobile
- 🔍 **Search functionality** to quickly find passwords
- 🎲 **Password generator** for creating secure passwords
- 📋 **One-click copy** to clipboard functionality
- 📝 **Add, edit, delete** password entries
- 🏷️ **Optional notes** for each password entry
- 🔐 **No plaintext storage** - everything is encrypted
- 🚀 **Easy deployment** to free hosting platforms

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Encryption**: Fernet (cryptography library)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Icons**: Bootstrap Icons
- **Hosting**: Ready for Render.com deployment

## 📦 Installation & Local Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Start
```bash
# Clone or download the project
git clone https://github.com/yourusername/password-manager.git
cd password-manager

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Open your browser and go to http://localhost:5000
```

## 🚀 Deployment to Render (Free Hosting)

### Method 1: Using GitHub (Recommended)
1. **Create a GitHub repository** and push your code
2. **Go to [Render.com](https://render.com)** and sign up
3. **Click "New" → "Web Service"**
4. **Connect your GitHub repository**
5. **Configure the service**:
   - Name: `password-manager`
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Instance Type: `Free`
6. **Click "Create Web Service"**

### Method 2: Manual Upload
1. **Create a GitHub repository** with your code
2. **Use the included `render.yaml`** file for automatic configuration
3. **Deploy directly from GitHub** to Render

## 🔐 Security Features

### Encryption
- **Fernet encryption** (AES-128 in CBC mode + HMAC)
- **All passwords encrypted** before storage
- **Encryption key** derived from your master password
- **No backdoors** - we cannot recover your data

### Authentication
- **Master password hashing** with salt
- **Secure session management**
- **CSRF protection**
- **No password recovery** (for security - we don't store your master password)

### Data Protection
- **Local file storage** (you control your data)
- **JSON format** for easy backup/export
- **Encrypted at rest** - files are encrypted on disk

## 📱 Usage Guide

### First Time Setup
1. Visit your deployed URL
2. Set your **master password** (this cannot be changed later!)
3. Remember this password - **it cannot be recovered if lost**

### Adding Passwords
1. Click **"Add Password"** button
2. Fill in the website, username, and password
3. Add optional notes if needed
4. Click **"Add Password"** to save

### Managing Passwords
- **View**: Click "View" to see password details
- **Edit**: Click "Edit" to modify entries
- **Delete**: Click "Delete" to remove entries
- **Search**: Use the search bar to find specific passwords
- **Copy**: Click the clipboard icon to copy passwords

### Password Generation
- Click the **shuffle icon** (🔀) next to password fields
- Generates **16-character secure passwords** with mixed case, numbers, and symbols

## 🔧 File Structure

```
password-manager/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── render.yaml        # Render deployment config
├── gunicorn_config.py # Gunicorn settings
├── templates/         # HTML templates
│   ├── base.html      # Base layout
│   ├── login.html     # Login page
│   └── dashboard.html # Main interface
├── static/            # Static files
│   └── style.css      # Custom styles
├── passwords.json     # Encrypted password storage (auto-created)
├── key.key           # Encryption key (auto-created)
└── master_password.hash # Master password hash (auto-created)
```

## 🚨 Important Security Notes

### ⚠️ Critical Warnings
- **Never share your master password** with anyone
- **Back up your data regularly** - download `passwords.json`
- **Use a strong master password** (12+ characters, mixed case, numbers, symbols)
- **Don't use common passwords** like "password123" or "admin"

### 🔒 Best Practices
- Use the **password generator** for new accounts
- **Don't reuse passwords** across different sites
- **Update passwords regularly** for important accounts
- **Enable 2FA** where possible on your accounts

### 📊 Free Hosting Limitations
- **File persistence**: Files may reset on free tier (back up regularly!)
- **Sleep time**: App sleeps after 15 minutes of inactivity
- **Monthly limits**: 750 hours free per month
- **Consider upgrading** for persistent storage

## 🔄 Backup & Recovery

### Manual Backup
1. **Download these files regularly**:
   - `passwords.json` (your encrypted passwords)
   - `key.key` (your encryption key)
2. **Store backups securely** (encrypted drive, cloud storage)
3. **Test restoration** periodically

### Recovery Process
If files are lost on free hosting:
1. **Redeploy the application**
2. **Set the same master password** (critical!)
3. **Upload your backed-up files**
4. **Your passwords should be accessible again**

## 🐛 Troubleshooting

### Common Issues

**"Invalid master password" error**
- Ensure you're using the correct master password
- Check if files were reset (free hosting limitation)
- Restore from backup if available

**"Password not found" error**
- Refresh the page
- Check if entry was accidentally deleted
- Verify search terms

**App sleeping/loading slowly**
- Normal behavior on free tier
- Wait 10-30 seconds for app to wake up
- Consider upgrading for better performance

### Getting Help
- Check the **browser console** for JavaScript errors
- Verify **file permissions** on your hosting platform
- Ensure **all dependencies** are installed correctly

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

## ⚖️ Disclaimer

This is a personal password manager for educational and personal use. While every effort has been made to ensure security, the authors are not responsible for any data loss or security breaches. Always maintain backups and use strong master passwords.

---

**Made with ❤️ for secure password management**
