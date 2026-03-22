import pyotp

def generate_totp_secret():
    return pyotp.random_base32()

def get_totp_uri(username, secret, issuer_name="ProyectoSeguridad"):
    return pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name=issuer_name)

def verify_totp(secret, token):
    totp = pyotp.TOTP(secret)
    return totp.verify(token)
