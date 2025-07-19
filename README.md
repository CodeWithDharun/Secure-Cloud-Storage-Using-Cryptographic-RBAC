# 🔐 Secure Cloud Storage System with Cryptographic Role-Based Access

This project is a secure cloud storage platform that implements **Cryptographic Role-Based Access Control (RBAC)**. It enables users to securely store, access, and manage files based on their assigned roles. The system is built using **Django (Python)** as the backend, **MySQL** for data storage, and **HTML/CSS** for the frontend interface.

---

## 📌 Key Features

- 🔒 Role-based access control (RBAC) for file sharing
- 🧾 File encryption before upload
- 🗂️ Organized storage system with user-level permissions
- ✅ Admin, Manager, and User roles with different privileges
- 📥 Secure file upload/download functionality
- 📊 User dashboard with access logs
- 🐍 Built using Django (Python), MySQL, HTML/CSS

---

## 📁 Project Structure


---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.x
- Django 4.x or newer
- MySQL Server
- MySQL Client Connector (`mysqlclient` or `PyMySQL`)
- Git

### ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/secure-cloud-storage.git
   cd secure-cloud-storage
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

pip install -r requirements.txt

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cloud_db',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

python manage.py runserver

| Role    | Access Rights                                  |
| ------- | ---------------------------------------------- |
| Admin   | Manage all users, view all files, assign roles |
| Manager | Upload/view department files, approve access   |
| User    | Upload and view personal files                 |


🔐 Security Features
Encrypted file storage using AES or RSA

Role-based authorization logic

Secure session and CSRF protection via Django

Password hashing using Django's built-in tools

📦 Dependencies
Django

MySQL

cryptography

mysqlclient or PyMySQL
