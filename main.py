import click
from flask.cli import with_appcontext
from src.app import DB, creat_app
from src.app.routes import routes
from src.app.db import populate_db
from flask_jwt_extended import JWTManager

from dotenv import load_dotenv
load_dotenv()

app = creat_app()
jwt = JWTManager(app)
routes(app)

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Cria e popula o banco de dados."""
    DB.create_all()
    populate_db()
    print("Banco de dados criado e populado com sucesso!")

app.cli.add_command(init_db_command)

@click.command(name='delete_tables')
@with_appcontext
def delete_tables():
  DB.drop_all()

app.cli.add_command(delete_tables)

if __name__ == "__main__":
    app.run(debug=True, port=8000)