from src.app import DB
from sqlalchemy.orm import Mapped, relationship

class Voos(DB.Model):
    __tablename__ = 'voos'

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    mes = DB.Column(DB.Integer, nullable=False)
    ano = DB.Column(DB.Integer, nullable=False)
    mercado = DB.Column(DB.String(100), nullable=False)
    rpk = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f"<Voo {self.mercado} - {self.mes}/{self.ano} | RPK: {self.rpk} >"
    
    def to_dict(self):
        return {
            "id": self.id,
            "ano": self.ano,
            "mes": self.mes,
            "mercado": self.mercado,
            "rpk": self.rpk
        }
    
class User(DB.Model):
    __tablename__ = 'users'
    id: Mapped[int] = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = DB.Column(DB.String, nullable=False)
    email: Mapped[str] = DB.Column(DB.String, nullable=False)
    password: Mapped[str] = DB.Column(DB.String, nullable=False)
    
    
    def as_dict(self):
        user_dict = {
            "id": self.id,
            "email": self.email
        }
        return user_dict