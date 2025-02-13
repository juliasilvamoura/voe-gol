
import plotly.express as px
import plotly.io as pio
import pandas as pd
import json
import os
from flask import request, jsonify, render_template, send_from_directory
from datetime import date
from src.app.controllers.filters import get_unic_mercados, get_mercado_by_name, get_voos_intervalo, get_voos_grafico
from src.app.controllers.user import create_user
from src.app.controllers.login import login_DB
from src.app.utils import generate_jwt
from flask_jwt_extended import jwt_required

def routes(app):
    @app.route("/", methods=["GET"])
    def home():
        return jsonify(message="API is working!")

    @app.route("/voos/mercado", methods=["GET", "POST"])
    def filter_mercado():
        if request.method == 'GET':
            mercados = get_unic_mercados()
            mercados = [mercado[0] for mercado in mercados]  
            if isinstance(mercados, dict) and "error" in mercados:
                return jsonify(mercados), 400
            return jsonify(mercados), 200
    
        elif request.method == 'POST':
            mercado = request.json.get('mercado')
            dados_filtrados = get_mercado_by_name(mercado)
            if isinstance(dados_filtrados, dict) and "error" in dados_filtrados:
                return jsonify(dados_filtrados), 400
            return jsonify(dados_filtrados), 200
        
        
    @app.route("/voos/intervalo", methods=["GET"])
    def filter_intervalo():
        ano_inicio = request.args.get('ano_inicio', type=int)
        mes_inicio = request.args.get('mes_inicio', type=int)
        ano_fim = request.args.get('ano_fim', type=int)
        mes_fim = request.args.get('mes_fim', type=int)


        if not (ano_inicio and mes_inicio):
            data_atual = date.today()
            ano_inicio = data_atual.year
            mes_inicio = data_atual.month
        
        if not (ano_inicio and mes_inicio and ano_fim and mes_fim):
            return jsonify({"error": "Informe um intervalo"}), 400
        
        voos = get_voos_intervalo(ano_inicio, mes_inicio, ano_fim, mes_fim)

        if isinstance(voos, dict) and "error" in voos:
            return jsonify(voos), 400  
        if not voos: 
            resposta = {"message": "Nenhum voo encontrado no intervalo selecionado."}
            return jsonify(resposta), 404
        
        return jsonify({"voos": [voo.to_dict() for voo in voos]})
    

    @app.route("/voos/grafico", methods=["GET", "POST"])
    def gerar_grafico():
        if request.method == "POST":
            ano_inicio = request.form.get('ano_inicio', type=int)
            mes_inicio = request.form.get('mes_inicio', type=int)
            ano_fim = request.form.get('ano_fim', type=int)
            mes_fim = request.form.get('mes_fim', type=int)
            mercado = request.form.get('mercado')

            if not (ano_inicio and mes_inicio and ano_fim and mes_fim):
                return jsonify({"error": "Informe um intervalo"}), 400

            voos = get_voos_grafico(ano_inicio, mes_inicio, ano_fim, mes_fim, mercado)

            if isinstance(voos, dict) and "error" in voos:
                return jsonify(voos), 400  
            if voos is None: 
                return jsonify({"message": "Nenhum voo encontrado para o intervalo"}), 404

            voos_df = pd.DataFrame(voos)
            
            voos_df['data'] = pd.to_datetime(voos_df[['ano', 'mes']].astype(str).agg('-'.join, axis=1) + '-01')
            voos_df['date'] = voos_df['data'].dt.strftime('%b/%y')

            voos_df_agrupado = voos_df.groupby('date').agg({'rpk': 'sum'}).reset_index()

            voos_df_agrupado['data_ordem'] = pd.to_datetime(voos_df_agrupado['date'], format='%b/%y')

            voos_df_agrupado = voos_df_agrupado.sort_values(by='data_ordem')


            fig = px.line(
                voos_df_agrupado, 
                x='date', 
                y='rpk',  
                title='Gráfico de RPK por Data'
            )

            fig.update_layout(
                xaxis_tickformat='%b/%Y',
            )
            
            graph_html = pio.to_html(fig, full_html=False)

            return render_template("grafico_voos.html", graph_html=graph_html)

        return render_template("grafico_voos.html")


    @app.route("/users", methods=["POST"])
    def post_user():
        body = request.get_json()
        new_user = create_user(body)
        if isinstance(new_user, dict) and "error" in new_user:
            return jsonify(new_user), 400  
        if new_user is None: 
            return jsonify({"error": "User not found"}), 404
        return jsonify(new_user.as_dict()), 201
    

    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email e senha são obrigatórios"}), 400
        
        user = login_DB(email,password)

        if not user:  
            return jsonify({"error": f"Credenciais inválidas"}), 401

        access_token = generate_jwt({"id": user.id, "name": user.name, "email": user.email})

        return jsonify({"token": access_token, "name": user.name, "email": user.email}), 200



    @app.route("/logout", methods=["POST"])
    @jwt_required()
    def logout():

        return jsonify({"message": "Logout realizado com sucesso!"}), 200

    @app.route("/swagger.json")
    def swagger_json():
        json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../static/swagger.json"))
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                swagger_data = json.load(file)
            return jsonify(swagger_data)
        except FileNotFoundError:
            return jsonify({"error": "swagger.json não encontrado"}), 404
        except json.JSONDecodeError:
            return jsonify({"error": "Erro ao ler swagger.json"}), 500
    
    @app.route("/swagger")
    def swagger_ui():
        return render_template("swagger.html")