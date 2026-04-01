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
    <body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f7fa; color: #2c3136; margin: 0; padding: 40px 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 4px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">
            <div style="background-color: #2c3136; padding: 25px; border-bottom: 5px solid #0056b3; text-align: center;">
                <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 600; letter-spacing: 1px;">SUT-BO</h1>
                <p style="color: #a0aab2; margin: 5px 0 0 0; font-size: 13px;">Sistema Único de Trámites Bolivia</p>
            </div>
            <div style="padding: 40px; border-top: 1px solid #e2e8f0;">
                <h2 style="color: #2c3136; margin-top: 0; font-size: 20px;">Identificación de Usuario</h2>
                <p style="color: #4a5568; line-height: 1.6;">Hola,</p>
                <p style="color: #4a5568; line-height: 1.6;">Ha solicitado un código de verificación para acceder a la Sede Electrónica. Por favor, utilice el siguiente código para completar su ingreso:</p>
                
                <div style="text-align: center; margin: 40px 0;">
                    <div style="display: inline-block; background-color: #f8fafc; border: 2px solid #e2e8f0; border-radius: 8px; padding: 20px 40px;">
                        <span style="font-size: 36px; font-weight: 700; color: #0056b3; letter-spacing: 8px; font-family: monospace;">
                            {otp_code}
                        </span>
                    </div>
                </div>
                
                <p style="color: #718096; font-size: 14px; margin-bottom: 0;">Este código tiene una validez de 10 minutos. No comparta este código con nadie.</p>
                <p style="color: #718096; font-size: 14px; margin-top: 5px;">Si no ha solicitado este acceso, puede ignorar este mensaje de forma segura.</p>
            </div>
            <div style="background-color: #f8fafc; padding: 20px; text-align: center; border-top: 1px solid #e2e8f0;">
                <p style="font-size: 12px; color: #a0aec0; margin: 0;">
                    © 2026 Plataforma de Identidad y Trámites Digitales - SUT-BO.<br>
                    Este es un correo automático, por favor no responda.
                </p>
            </div>
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
