from app import create_app
from extensions import db
from models.role import Role
from models.user import User

app = create_app()

def init_db():
    with app.app_context():
        # 1. Borrar todos los registros existentes (limpiar BD)
        print("Borrando base de datos existente...")
        db.drop_all()
        
        # 2. Crear todas las tablas
        print("Creando tablas...")
        db.create_all()
        
        # 3. Crear roles por defecto
        print("Creando roles...")
        roles = {
            'USER': Role(name='USER'),
            'ADMIN': Role(name='ADMIN'),
            'AUDITOR': Role(name='AUDITOR')
        }
        for role in roles.values():
            db.session.add(role)
        
        # 4. Crear usuarios solicitados
        print("Creando usuarios por defecto...")
        users_data = [
            {
                'carnet': '1234567', 
                'email': 'admin@example.com', 
                'role': 'ADMIN',
                'names': 'Administrador',
                'paternal_surname': 'Sistema',
                'maternal_surname': 'SUT'
            },
            {
                'carnet': '7654321', 
                'email': 'auditor@example.com', 
                'role': 'AUDITOR',
                'names': 'Auditor',
                'paternal_surname': 'Transparencia',
                'maternal_surname': 'Nacional'
            },
            {
                'carnet': '1010101', 
                'email': 'user@example.com', 
                'role': 'USER',
                'names': 'Juan',
                'paternal_surname': 'Ciudadano',
                'maternal_surname': 'Boliviano'
            },
        ]
        
        password = "password123!"
        
        for data in users_data:
            user = User(
                carnet=data['carnet'], 
                email=data['email'],
                names=data['names'],
                paternal_surname=data['paternal_surname'],
                maternal_surname=data['maternal_surname']
            )
            user.set_password(password)
            user.roles.append(roles[data['role']])
            db.session.add(user)
        
        db.session.commit()
        print("Base de datos inicializada con éxito!")
        print("CIs creados: 1234567 (Admin), 7654321 (Auditor), 1010101 (User)")
        print(f"Contraseña común: {password}")

if __name__ == "__main__":
    init_db()
