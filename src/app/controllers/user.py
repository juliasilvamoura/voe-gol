from werkzeug.security import generate_password_hash
from src.app import DB
from src.app.models import User

def create_user(body):
    # Valida se todos os campos obrigatórios estão presentes
    required_fields = ["name", "email", "password"]
    for field in required_fields:
        if field not in body:
            return {"error":f"'{field}' is required"}
    
    # Valida se o email já está em uso
    if User.query.filter_by(email=body['email']).first():
        return {"error": "Email already in use"}

    password = body.get("password", "").strip()
    hashed_password = generate_password_hash(password)

    new_user = User(
        name=body['name'],
        email=body['email'],
        password=hashed_password
    )
    DB.session.add(new_user)
    DB.session.commit()
    return new_user