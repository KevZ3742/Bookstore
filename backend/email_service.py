import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Mailtrap SMTP Configuration
MAILTRAP_HOST = "sandbox.smtp.mailtrap.io"
MAILTRAP_PORT = 2525
MAILTRAP_USERNAME = "1a7fb7b7abb6d0"
MAILTRAP_PASSWORD = "58a35bc932834e"

def send_checkout_email(customer_email, customer_name, items, total):
    """
    Send checkout confirmation email to customer.
    
    Args:
        customer_email: Customer's email address
        customer_name: Customer's username
        items: List of purchased items [{"title": str, "author": str, "type": str, "cost": float}]
        total: Total cost of the order
    """
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Order Confirmation - Bookstore'
        msg['From'] = 'bookstore@example.com'
        msg['To'] = customer_email
        
        # Build the email body
        html_body = build_email_html(customer_name, items, total)
        text_body = build_email_text(customer_name, items, total)
        
        # Attach both plain text and HTML versions
        part1 = MIMEText(text_body, 'plain')
        part2 = MIMEText(html_body, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email via Mailtrap
        with smtplib.SMTP(MAILTRAP_HOST, MAILTRAP_PORT) as server:
            server.login(MAILTRAP_USERNAME, MAILTRAP_PASSWORD)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
        
        return True, "Email sent successfully"
    
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False, str(e)


def build_email_text(customer_name, items, total):
    """Build plain text version of the email."""
    text = f"""
Dear {customer_name},

Thank you for your order!

ORDER SUMMARY:
{'='*50}
"""
    
    for item in items:
        text += f"""
Title: {item['title']}
Author: {item['author']}
Type: {item['type'].upper()}
Cost: ${item['cost']:.2f}
{'-'*50}
"""
    
    text += f"""
TOTAL: ${total:.2f}
{'='*50}

Your order has been processed successfully. 

Thank you for shopping with us!

Best regards,
Bookstore Team
"""
    return text


def build_email_html(customer_name, items, total):
    """Build HTML version of the email."""
    
    items_html = ""
    for item in items:
        items_html += f"""
        <tr>
            <td style="padding: 12px; border-bottom: 1px solid #eee;">{item['title']}</td>
            <td style="padding: 12px; border-bottom: 1px solid #eee;">{item['author']}</td>
            <td style="padding: 12px; border-bottom: 1px solid #eee; text-transform: uppercase;">{item['type']}</td>
            <td style="padding: 12px; border-bottom: 1px solid #eee; text-align: right;">${item['cost']:.2f}</td>
        </tr>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background-color: #4CAF50; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0;">
            <h1 style="margin: 0;">Order Confirmation</h1>
        </div>
        
        <div style="background-color: #f9f9f9; padding: 20px; border: 1px solid #ddd; border-top: none;">
            <p>Dear <strong>{customer_name}</strong>,</p>
            <p>Thank you for your order! Here's a summary of your purchase:</p>
            
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0; background-color: white;">
                <thead>
                    <tr style="background-color: #f2f2f2;">
                        <th style="padding: 12px; text-align: left; border-bottom: 2px solid #ddd;">Title</th>
                        <th style="padding: 12px; text-align: left; border-bottom: 2px solid #ddd;">Author</th>
                        <th style="padding: 12px; text-align: left; border-bottom: 2px solid #ddd;">Type</th>
                        <th style="padding: 12px; text-align: right; border-bottom: 2px solid #ddd;">Cost</th>
                    </tr>
                </thead>
                <tbody>
                    {items_html}
                </tbody>
                <tfoot>
                    <tr style="background-color: #f2f2f2; font-weight: bold;">
                        <td colspan="3" style="padding: 12px; text-align: right;">TOTAL:</td>
                        <td style="padding: 12px; text-align: right;">${total:.2f}</td>
                    </tr>
                </tfoot>
            </table>
            
            <p>Your order has been processed successfully.</p>
            <p>Thank you for shopping with us!</p>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px;">
                <p>Best regards,<br><strong>Bookstore Team</strong></p>
                <p style="margin-top: 20px;">Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html