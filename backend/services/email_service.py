from typing import Dict, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """
    Service for sending emails including password reset emails
    """

    @staticmethod
    def send_password_reset_email(to_email: str, reset_token: str) -> bool:
        """
        Send a password reset email to the user

        Args:
            to_email: Recipient's email address
            reset_token: Password reset token to include in the reset link

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            # Build the reset link
            reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

            # Create the email content
            subject = "Password Reset Request - Todo Pro"
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    .header {{ text-align: center; margin-bottom: 30px; }}
                    .button {{ display: inline-block; padding: 12px 30px; background-color: #4F46E5; color: white !important; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
                    .footer {{ margin-top: 30px; text-align: center; color: #6B7280; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1 style="color: #1F2937;">Todo Pro</h1>
                        <h2>Password Reset Request</h2>
                    </div>

                    <p>Hello,</p>

                    <p>We received a request to reset your password for your Todo Pro account. Click the button below to reset your password:</p>

                    <div style="text-align: center;">
                        <a href="{reset_link}" class="button">Reset Password</a>
                    </div>

                    <p>Or copy and paste this link into your browser:</p>
                    <p><a href="{reset_link}">{reset_link}</a></p>

                    <p>This link will expire in 1 hour for security reasons.</p>

                    <p>If you didn't request a password reset, you can safely ignore this email.</p>

                    <div class="footer">
                        <p>This is an automated message from Todo Pro. Please do not reply to this email.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            text_content = f"""
            Password Reset Request

            We received a request to reset your password for your Todo Pro account.

            Click the link below to reset your password:
            {reset_link}

            This link will expire in 1 hour for security reasons.

            If you didn't request a password reset, you can safely ignore this email.
            """

            # In development, we'll just log the email instead of sending it
            if settings.ENVIRONMENT == "development":
                logger.info(f"Password reset email would be sent to: {to_email}")
                logger.info(f"Reset link: {reset_link}")
                print(f"\n--- MOCK EMAIL SENT ---")
                print(f"To: {to_email}")
                print(f"Subject: {subject}")
                print(f"Reset Link: {reset_link}")
                print(f"----------------------\n")
                return True

            # For production, send the actual email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = settings.EMAIL_SENDER
            msg['To'] = to_email

            # Create both text and HTML parts
            text_part = MIMEText(text_content, 'plain')
            html_part = MIMEText(html_content, 'html')

            msg.attach(text_part)
            msg.attach(html_part)

            # Connect to SMTP server and send email
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)

                server.send_message(msg)

            logger.info(f"Password reset email sent successfully to: {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send password reset email to {to_email}: {str(e)}")
            return False

    @staticmethod
    def send_test_email(to_email: str, subject: str = "Test Email", message: str = "This is a test email.") -> bool:
        """
        Send a test email (for development/testing purposes)
        """
        try:
            if settings.ENVIRONMENT == "development":
                print(f"\n--- MOCK TEST EMAIL ---")
                print(f"To: {to_email}")
                print(f"Subject: {subject}")
                print(f"Message: {message}")
                print(f"----------------------\n")
                return True

            # Actual email sending logic would go here
            # For now, just returning True in dev mode
            return True
        except Exception as e:
            logger.error(f"Failed to send test email to {to_email}: {str(e)}")
            return False