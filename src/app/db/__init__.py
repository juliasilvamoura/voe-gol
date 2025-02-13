from werkzeug.security import generate_password_hash
from src.app.utils import is_table_empty
from src.app.models import User
from src.app import DB

users = [
    {"name": "Julia","email": "julia.teste@gmail.com", "password": "senha123"},
    {"name": "Juliana","email": "juliaana.teste@gmail.com", "password": "senha123"}
]

def populate_db_users():
    if is_table_empty(User.query.first(), 'users'):
        for user in users:
            user['password'] = generate_password_hash(user['password'])
            new_user = User(**user)
            DB.session.add(new_user)
        DB.session.commit()
        print("Users populated")

def populate_db():
    populate_db_users()