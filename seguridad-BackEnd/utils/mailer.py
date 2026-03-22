import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_otp_email(to_email, otp_code):
    smtp_server = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('MAIL_PORT', 587))
    smtp_user = os.getenv('MAIL_USERNAME')
    smtp_password = os.getenv('MAIL_PASSWORD')
    
    subject = "Tu Código de Verificación Segura"
    body = f"""
    <html>
    <body style="font-family: sans-serif; background-color: #0d0d0d; color: #ffffff; padding: 20px;">
        <div style="max-width: 500px; margin: auto; border: 1px solid #0096ff; border-radius: 15px; padding: 30px; background-color: #111111;">
            <h2 style="color: #0096ff; text-align: center;">Seguridad Proyecto</h2>
            <p>Hola,</p>
            <p>Has solicitado un código de verificación para acceder a tu cuenta.</p>
            <div style="text-align: center; margin: 30px 0;">
                <span style="font-size: 32px; font-weight: bold; color: #0096ff; letter-spacing: 5px; border: 2px dashed #0096ff; padding: 10px 20px;">
                    {otp_code}
                </span>
            </div>
            <p style="color: #888; font-size: 14px;">Este código expirará en 10 minutos. Si no solicitaste este código, por favor ignora este correo.</p>
            <hr style="border: 0; border-top: 1px solid #333; margin: 20px 0;">
            <p style="text-align: center; font-size: 12px; color: #555;">&copy; 2026 Seguridad Proyecto. Todos los derechos reservados.</p>
        </div>
    </body>
    </html>
    """
    
    msg = MIMEMultipart()
    msg['From'] = f"Seguridad Proyecto <{smtp_user}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'html'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
