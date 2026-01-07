"""
Email Service for sending newsletters
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
from app.config import settings

class EmailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.email_from = settings.EMAIL_FROM
    
    def _create_newsletter_html(self, topic: str, articles: List[Dict[str, Any]]) -> str:
        """
        Create HTML newsletter from articles
        """
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px;
                }}
                .article {{
                    border-bottom: 1px solid #eee;
                    padding: 20px 0;
                }}
                .article:last-child {{
                    border-bottom: none;
                }}
                .article h2 {{
                    color: #4CAF50;
                    margin-top: 0;
                }}
                .article img {{
                    max-width: 100%;
                    height: auto;
                    border-radius: 5px;
                }}
                .source {{
                    color: #666;
                    font-size: 0.9em;
                }}
                .read-more {{
                    display: inline-block;
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-top: 10px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    color: #666;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{topic} Industry Newsletter</h1>
                <p>Your latest industry news digest</p>
            </div>
        """
        
        for idx, article in enumerate(articles, 1):
            html += f"""
            <div class="article">
                <h2>{idx}. {article['title']}</h2>
                <p class="source">Source: {article['source']} | Published: {article['published_at']}</p>
                {f'<img src="{article["image_url"]}" alt="Article Image">' if article.get('image_url') else ''}
                <p class="summary">{article.get('summary', article.get('description', ''))}</p>
                <p>{article.get('description', '')}</p>
                <a href="{article['url']}" class="read-more" target="_blank">Read Full Article</a>
            </div>
            """
        
        html += """
            <div class="footer">
                <p>This newsletter was sent to you because you subscribed to {topic} updates.</p>
                <p>If you wish to unsubscribe, please contact us.</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def send_newsletter(self, to_email: str, topic: str, articles: List[Dict[str, Any]]):
        """
        Send newsletter email
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"{topic} Industry Newsletter - Top Stories"
            msg['From'] = self.email_from
            msg['To'] = to_email
            
            # Create HTML body
            html_body = self._create_newsletter_html(topic, articles)
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Send email
            recipients = [to_email]
            # In DEBUG mode, also BCC the configured SMTP user (useful for Ethereal testing)
            try:
                from app.config import settings
                if getattr(settings, 'DEBUG', False) and self.smtp_user not in recipients:
                    recipients.append(self.smtp_user)
                    msg['Bcc'] = self.smtp_user
            except Exception:
                pass

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg, from_addr=self.email_from, to_addrs=recipients)
                print(f"Email sent to recipients: {recipients}")
            
            print(f"Newsletter sent successfully to {to_email}")
            return True
            
        except Exception as e:
            print(f"Error sending email to {to_email}: {str(e)}")
            return False
