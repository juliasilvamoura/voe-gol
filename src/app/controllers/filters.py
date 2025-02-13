from src.app import DB
from src.app.models import Voos

def get_unic_mercados():
    try:
        query = Voos.query.with_entities(Voos.mercado).distinct().all()
        return query
    except Exception as e:
        return {"error": f"{e}"}
    
def get_mercado_by_name(mercado_selecionado):
    try:
        query = Voos.query.filter_by(mercado=mercado_selecionado).all()
        return [voo.to_dict() for voo in query]
    except Exception as e:
        return {"error": f"{e}"}
    
def get_voos_intervalo(ano_inicio, mes_inicio, ano_fim, mes_fim):
    try:
        query = Voos.query.filter(
            (Voos.ano > ano_inicio) | ((Voos.ano == ano_inicio) & (Voos.mes >= mes_inicio)),
            (Voos.ano < ano_fim) | ((Voos.ano == ano_fim) & (Voos.mes <= mes_fim))
        )
        query = query.all()
        return query
    except Exception as e:
        return {"error": f"{e}"}
    
def get_voos_grafico(ano_inicio, mes_inicio, ano_fim, mes_fim, mercado_selecionado):
    try:
        query = Voos.query.filter(
            (Voos.ano > ano_inicio) | ((Voos.ano == ano_inicio) & (Voos.mes >= mes_inicio)),
            (Voos.ano < ano_fim) | ((Voos.ano == ano_fim) & (Voos.mes <= mes_fim)),
            (Voos.mercado == mercado_selecionado)
        )
        query = query.all()

        voos_data = [{
            'ano': voo.ano,
            'mes': voo.mes,
            'rpk': voo.rpk,
            'mercado': voo.mercado
        } for voo in query]


        return voos_data
    except Exception as e:
        return {"error": f"{e}"}