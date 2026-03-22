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
            {'username': 'admin', 'email': 'admin@example.com', 'role': 'ADMIN'},
            {'username': 'auditor', 'email': 'auditor@example.com', 'role': 'AUDITOR'},
            {'username': 'user', 'email': 'user@example.com', 'role': 'USER'},
        ]
        
        password = "password123!"
        
        for data in users_data:
            user = User(username=data['username'], email=data['email'])
            user.set_password(password)
            user.roles.append(roles[data['role']])
            db.session.add(user)
        
        db.session.commit()
        print("Base de datos inicializada con éxito!")
        print(f"Usuarios creados: admin@example.com, auditor@example.com, user@example.com")
        print(f"Contraseña común: {password}")

if __name__ == "__main__":
    init_db()
