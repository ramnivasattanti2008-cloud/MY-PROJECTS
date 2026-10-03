# Password Vault

A Flask application for securely storing passwords with Fernet encryption.

## Features

- **Master Password** - Single password to unlock the vault
- **Fernet Encryption** - Passwords encrypted using cryptography library
- **Add/Edit/Delete** - Full CRUD operations for password entries
- **Search & Filter** - Find passwords by title, username, or tags
- **Tag Organization** - Organize passwords with tags
- **Dark Theme** - Modern dark interface
- **Copy to Clipboard** - Quick copy functionality

## Installation

```bash
cd password-vault
pip install -r requirements.txt
python app.py
```

## Usage

1. Run `python app.py`
2. Opens at `http://localhost:5000`
3. On first run, create a master password
4. Add passwords with title, username, password, URL, tags, and notes
5. Click on any entry to view and copy the password

## Security

- Master password is hashed using SHA-256
- Individual passwords are encrypted using Fernet (AES-128-CBC)
- Encryption key is stored in `vault.key` file
- Sessions expire when browser closes

## Database

SQLite database (`vault.db`) and encryption key (`vault.key`) created automatically.
Keep the `vault.key` file safe - losing it means losing access to all passwords.

## Project Structure

```
password-vault/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── setup.html
│   ├── login.html
│   ├── add_entry.html
│   ├── view_entry.html
│   └── edit_entry.html
└── README.md
```

## Warning

Do not lose the `vault.key` file. Without it, your encrypted passwords cannot be recovered.
