from src.app.models import User
from werkzeug.security import check_password_hash
from flask import  jsonify

def login_DB(email, password):
    try:
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return None
        
        return user
    except Exception as e:
        return {"error": f"{e}"}