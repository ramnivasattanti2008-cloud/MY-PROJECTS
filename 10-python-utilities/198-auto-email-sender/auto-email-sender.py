#!/usr/bin/env python3
"""
Auto Email Sender - Send emails with Python using SMTP (Gmail)

Features:
- Send plain text and HTML emails
- Attach files (images, documents, etc.)
- Support for email templates
- BCC support for mass sending
- CC support
- Error handling and validation

Usage:
    python auto-email-sender.py --to recipient@example.com --subject "Hello" --body "Message"
    python auto-email-sender.py --config config.json --template template.html
"""

import argparse
import json
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import Optional

# Try to import keyring for secure password storage
try:
    import keyring
    HAS_KEYRING = True
except ImportError:
    HAS_KEYRING = False


class EmailSender:
    """Handles sending emails via SMTP with Gmail."""

    def __init__(self, sender_email: str, sender_password: str,
                 smtp_server: str = "smtp.gmail.com",
                 smtp_port: int = 587):
        """
        Initialize the email sender.

        Args:
            sender_email: Sender's email address
            sender_password: App password or OAuth token
            smtp_server: SMTP server address
            smtp_port: SMTP port (587 for TLS, 465 for SSL)
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    @classmethod
    def from_config(cls, config_path: str) -> 'EmailSender':
        """
        Create EmailSender from a JSON configuration file.

        Args:
            config_path: Path to JSON config file

        Returns:
            EmailSender instance
        """
        with open(config_path, 'r') as f:
            config = json.load(f)

        return cls(
            sender_email=config['sender_email'],
            sender_password=config['sender_password'],
            smtp_server=config.get('smtp_server', 'smtp.gmail.com'),
            smtp_port=config.get('smtp_port', 587)
        )

    def _connect(self) -> smtplib.SMTP:
        """Establish SMTP connection with TLS."""
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.sender_email, self.sender_password)
            return server
        except smtplib.SMTPAuthenticationError:
            raise ValueError("Authentication failed. Check your email and app password.")
        except smtplib.SMTPException as e:
            raise RuntimeError(f"SMTP connection failed: {e}")

    def send_email(
        self,
        to: list[str],
        subject: str,
        body: str = None,
        html_body: str = None,
        cc: list[str] = None,
        bcc: list[str] = None,
        attachments: list[str] = None,
        from_name: str = None
    ) -> bool:
        """
        Send an email with optional attachments and HTML content.

        Args:
            to: List of recipient email addresses
            subject: Email subject line
            body: Plain text body (optional if html_body provided)
            html_body: HTML body (optional if body provided)
            cc: List of CC recipients
            bcc: List of BCC recipients
            attachments: List of file paths to attach
            from_name: Display name for sender

        Returns:
            True if email sent successfully
        """
        if not body and not html_body:
            raise ValueError("Either 'body' or 'html_body' must be provided")

        # Create message container
        msg = MIMEMultipart('mixed')
        msg['From'] = f"{from_name} <{self.sender_email}>" if from_name else self.sender_email
        msg['To'] = ', '.join(to)

        all_recipients = to.copy()
        if cc:
            msg['Cc'] = ', '.join(cc)
            all_recipients.extend(cc)
        if bcc:
            all_recipients.extend(bcc)

        msg['Subject'] = subject

        # Create alternative part (plain + HTML)
        msg_alternative = MIMEMultipart('alternative')
        if body:
            msg_alternative.attach(MIMEText(body, 'plain', 'utf-8'))
        if html_body:
            msg_alternative.attach(MIMEText(html_body, 'html', 'utf-8'))
        msg.attach(msg_alternative)

        # Add attachments
        if attachments:
            for filepath in attachments:
                if not os.path.exists(filepath):
                    print(f"Warning: Attachment not found: {filepath}")
                    continue

                with open(filepath, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())

                encoders.encode_base64(part)
                filename = os.path.basename(filepath)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{filename}"'
                )
                msg.attach(part)

        # Send the email
        try:
            server = self._connect()
            server.sendmail(self.sender_email, all_recipients, msg.as_string())
            server.quit()
            print(f"Email sent successfully to {len(to)} recipient(s)")
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to send email: {e}")

    def send_with_template(
        self,
        to: list[str],
        subject: str,
        template_path: str,
        template_data: dict,
        attachments: list[str] = None
    ) -> bool:
        """
        Send an email using a template file with variable substitution.

        Templates support {{variable}} syntax for substitution.

        Args:
            to: List of recipient email addresses
            subject: Email subject line
            template_path: Path to template file (.txt or .html)
            template_data: Dictionary of variables for template
            attachments: List of file paths to attach

        Returns:
            True if email sent successfully
        """
        template_path = Path(template_path)

        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        # Read template
        content = template_path.read_text(encoding='utf-8')

        # Substitute variables
        for key, value in template_data.items():
            placeholder = f"{{{{{key}}}}}"
            content = content.replace(placeholder, str(value))

        # Determine if HTML or plain text
        if template_path.suffix.lower() == '.html':
            html_body = content
            body = None
        else:
            body = content
            html_body = None

        return self.send_email(
            to=to,
            subject=subject,
            body=body,
            html_body=html_body,
            attachments=attachments
        )

    def send_mass_email(
        self,
        recipients: list[dict],
        subject_template: str,
        body_template: str = None,
        html_template: str = None
    ) -> int:
        """
        Send personalized emails to multiple recipients.

        Args:
            recipients: List of dicts with 'email' and other personalization data
            subject_template: Subject with {{variable}} placeholders
            body_template: Plain text body with placeholders
            html_template: HTML body with placeholders

        Returns:
            Number of emails successfully sent
        """
        success_count = 0

        for recipient in recipients:
            email = recipient.get('email')
            if not email:
                print("Warning: Skipping recipient without email")
                continue

            # Substitute recipient data into templates
            subject = self._substitute_template(subject_template, recipient)
            body = self._substitute_template(body_template, recipient) if body_template else None
            html = self._substitute_template(html_template, recipient) if html_template else None

            try:
                self.send_email(
                    to=[email],
                    subject=subject,
                    body=body,
                    html_body=html
                )
                success_count += 1
            except Exception as e:
                print(f"Failed to send to {email}: {e}")

        return success_count

    def _substitute_template(self, template: str, data: dict) -> str:
        """Substitute {{variable}} placeholders in template."""
        if not template:
            return None
        result = template
        for key, value in data.items():
            result = result.replace(f"{{{{{key}}}}}", str(value))
        return result


def create_config_file(config_path: str = "email_config.json"):
    """
    Create a template configuration file.

    Args:
        config_path: Path where to save the config file
    """
    config = {
        "sender_email": "your-email@gmail.com",
        "sender_password": "your-app-password",
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587
    }

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

    print(f"Configuration template created at: {config_path}")
    print("Please edit it with your Gmail credentials.")


def create_html_template(template_path: str = "email_template.html"):
    """
    Create a sample HTML email template.

    Args:
        template_path: Path where to save the template
    """
    template = """<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #4A90D9; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f9f9f9; }
        .footer { padding: 10px; text-align: center; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{title}}</h1>
        </div>
        <div class="content">
            <p>Dear {{name}},</p>
            <p>{{message}}</p>
            <p>Best regards,<br>{{sender_name}}</p>
        </div>
        <div class="footer">
            <p>This email was sent automatically.</p>
        </div>
    </div>
</body>
</html>"""

    with open(template_path, 'w') as f:
        f.write(template)

    print(f"Sample HTML template created at: {template_path}")


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description='Send emails via SMTP with Gmail',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Configuration options
    config_group = parser.add_argument_group('Configuration')
    config_group.add_argument('--config', '-c', help='Path to JSON config file')
    config_group.add_argument('--create-config', action='store_true',
                              help='Create a template config file')

    # Email content
    content_group = parser.add_argument_group('Email Content')
    content_group.add_argument('--to', '-t', nargs='+', required=True,
                               help='Recipient email address(es)')
    content_group.add_argument('--subject', '-s', required=True,
                               help='Email subject line')
    content_group.add_argument('--body', '-b', help='Plain text body')
    content_group.add_argument('--html', help='HTML body content')
    content_group.add_argument('--cc', nargs='+', help='CC recipients')
    content_group.add_argument('--bcc', nargs='+', help='BCC recipients')

    # Template options
    template_group = parser.add_argument_group('Template Options')
    template_group.add_argument('--template', help='Path to template file')
    template_group.add_argument('--template-data', type=json.loads,
                                 help='JSON string with template variables')
    template_group.add_argument('--create-template', action='store_true',
                                help='Create a sample HTML template')

    # Attachments
    parser.add_argument('--attach', '-a', nargs='+',
                         help='File path(s) to attach')

    # Sender info
    sender_group = parser.add_argument_group('Sender Info')
    sender_group.add_argument('--from', dest='from_name',
                               help='Sender display name')
    sender_group.add_argument('--email', help='Sender email (if not in config)')
    sender_group.add_argument('--password', help='Sender password (if not in config)')

    args = parser.parse_args()

    # Handle special commands
    if args.create_config:
        create_config_file()
        return

    if args.create_template:
        create_html_template()
        return

    # Load configuration
    if args.config:
        if not os.path.exists(args.config):
            print(f"Error: Config file not found: {args.config}")
            sys.exit(1)
        sender = EmailSender.from_config(args.config)
    else:
        # Check for credentials in arguments or environment
        email = args.email or os.environ.get('SMTP_EMAIL')
        password = args.password or os.environ.get('SMTP_PASSWORD')

        if not email or not password:
            print("Error: Email and password required.")
            print("Use --config file or --email/--password arguments")
            sys.exit(1)

        sender = EmailSender(email, password)

    # Prepare email content
    try:
        if args.template:
            # Using template
            template_data = args.template_data or {}
            sender.send_with_template(
                to=args.to,
                subject=args.subject,
                template_path=args.template,
                template_data=template_data,
                attachments=args.attach
            )
        else:
            # Direct email
            sender.send_email(
                to=args.to,
                subject=args.subject,
                body=args.body,
                html_body=args.html,
                cc=args.cc,
                bcc=args.bcc,
                attachments=args.attach,
                from_name=args.from_name
            )

        print("Email sent successfully!")

    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
