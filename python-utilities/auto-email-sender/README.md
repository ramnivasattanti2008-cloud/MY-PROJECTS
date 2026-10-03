# Auto Email Sender

A Python tool for sending emails via SMTP (Gmail) with support for attachments, HTML content, and email templates.

## Features

- Send plain text and HTML emails
- Attach multiple files
- Use email templates with variable substitution
- Send mass personalized emails
- CC and BCC support
- Configuration file support
- Error handling

## Installation

```bash
pip install -r requirements.txt
```

## Gmail Setup

To send emails via Gmail, you need an **App Password**:

1. Enable 2-Factor Authentication on your Google Account
2. Go to: https://myaccount.google.com/security
3. Select "App passwords" under "Signing in to Google"
4. Create a new app password for "Mail"
5. Use this 16-character password (without spaces) in the script

## Quick Start

### 1. Create a configuration file

```bash
# Create template config
python auto-email-sender.py --create-config
```

Edit `email_config.json` with your credentials:
```json
{
    "sender_email": "your-email@gmail.com",
    "sender_password": "xxxx xxxx xxxx xxxx",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
}
```

### 2. Send a simple email

```bash
python auto-email-sender.py \
    --config email_config.json \
    --to recipient@example.com \
    --subject "Hello World" \
    --body "This is a test email sent from Python!"
```

### 3. Send HTML email

```bash
python auto-email-sender.py \
    --config email_config.json \
    --to recipient@example.com \
    --subject "Beautiful Email" \
    --html "<h1>Hello!</h1><p>This is <strong>HTML</strong> content.</p>"
```

### 4. Send with attachments

```bash
python auto-email-sender.py \
    --config email_config.json \
    --to recipient@example.com \
    --subject "Check this out" \
    --body "Please see the attached files." \
    --attach document.pdf image.png
```

### 5. Send using a template

Create a template file (`template.html`):
```html
<!DOCTYPE html>
<html>
<body>
    <h1>Hello {{name}}!</h1>
    <p>Your order #{{order_id}} has been shipped.</p>
</body>
</html>
```

Send with template:
```bash
python auto-email-sender.py \
    --config email_config.json \
    --to recipient@example.com \
    --subject "Order Shipped" \
    --template template.html \
    --template-data '{"name": "John", "order_id": "12345"}'
```

### 6. CC and BCC

```bash
python auto-email-sender.py \
    --config email_config.json \
    --to recipient@example.com \
    --cc manager@company.com \
    --bcc archive@company.com \
    --subject "Report" \
    --body "Monthly report attached."
```

## Using as a Python Module

```python
from auto-email-sender import EmailSender

# Create sender with credentials
sender = EmailSender(
    sender_email="your-email@gmail.com",
    sender_password="app-password"
)

# Send simple email
sender.send_email(
    to=["recipient@example.com"],
    subject="Hello",
    body="Plain text message"
)

# Send HTML email
sender.send_email(
    to=["recipient@example.com"],
    subject="HTML Email",
    html_body="<h1>Title</h1><p>Content</p>"
)

# Send with template
sender.send_with_template(
    to=["recipient@example.com"],
    subject="Welcome",
    template_path="welcome.html",
    template_data={"name": "John", "code": "ABC123"}
)

# Send mass personalized emails
recipients = [
    {"email": "user1@example.com", "name": "Alice", "code": "001"},
    {"email": "user2@example.com", "name": "Bob", "code": "002"},
]
sender.send_mass_email(
    recipients=recipients,
    subject_template="Your code: {{code}}",
    body_template="Hello {{name}}, here is your code."
)
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `--config, -c` | Path to JSON configuration file |
| `--to, -t` | Recipient email address(es) (required) |
| `--subject, -s` | Email subject line (required) |
| `--body, -b` | Plain text body |
| `--html` | HTML body content |
| `--cc` | CC recipient(s) |
| `--bcc` | BCC recipient(s) |
| `--attach, -a` | Files to attach |
| `--template` | Path to template file |
| `--template-data` | JSON string with template variables |
| `--from` | Sender display name |
| `--email` | Sender email (alternative to config) |
| `--password` | Sender password (alternative to config) |
| `--create-config` | Create template config file |
| `--create-template` | Create sample HTML template |

## Environment Variables

You can also use environment variables for credentials:

```bash
export SMTP_EMAIL="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
python auto-email-sender.py --to recipient@example.com --subject "Test" --body "Hello"
```

## Troubleshooting

**"Authentication failed"**
- Make sure you're using an App Password, not your regular Gmail password
- Enable 2-Factor Authentication on your Google account
- Check that the app password is correct

**"SMTP connection failed"**
- Check your internet connection
- Verify SMTP server and port settings
- Some networks block port 587; try port 465

**"Less secure app access"**
- Gmail has deprecated less secure apps
- Always use App Passwords with 2FA enabled

## Security Notes

- Never commit configuration files with real credentials to version control
- Add `email_config.json` to your `.gitignore`
- Consider using environment variables for production
- App passwords should be treated like regular passwords

## License

MIT License
