"""
Ferramentas simuladas para os agentes de planejamento de viagem.
Estas são funções simples que simulam APIs externas sem necessidade de integrações reais.
"""

def consultar_clima(destino: str, data: str) -> str:
    """
    Simula consulta de clima para um destino e data.
    
    Args:
        destino: Nome da cidade
        data: Data no formato YYYY-MM-DD
        
    Returns:
        String com informações do clima
    """
    # Simulação simples baseada no destino
    climas = {
        "paris": "Ensolarado, 22°C",
        "tokyo": "Nublado, 18°C",
        "nova york": "Chuvoso, 15°C",
        "rio de janeiro": "Ensolarado, 28°C",
        "londres": "Nublado, 12°C"
    }
    
    destino_lower = destino.lower()
    clima = climas.get(destino_lower, "Temperatura amena, 20°C")
    
    return f"Clima em {destino} em {data}: {clima}"


def calcular_orcamento(destino: str, dias: int, tipo_hospedagem: str = "hotel") -> dict:
    """
    Simula cálculo de orçamento para uma viagem.
    
    Args:
        destino: Nome da cidade
        dias: Número de dias
        tipo_hospedagem: Tipo de hospedagem (hotel, hostel, airbnb)
        
    Returns:
        Dicionário com detalhes do orçamento
    """
    # Valores simulados por dia
    custos_base = {
        "paris": {"hotel": 150, "hostel": 40, "airbnb": 80, "comida": 50, "transporte": 30},
        "tokyo": {"hotel": 120, "hostel": 35, "airbnb": 70, "comida": 40, "transporte": 25},
        "nova york": {"hotel": 180, "hostel": 50, "airbnb": 100, "comida": 60, "transporte": 35},
        "rio de janeiro": {"hotel": 80, "hostel": 25, "airbnb": 50, "comida": 30, "transporte": 20},
        "londres": {"hotel": 140, "hostel": 45, "airbnb": 75, "comida": 45, "transporte": 28}
    }
    
    destino_lower = destino.lower()
    custos = custos_base.get(destino_lower, {
        "hotel": 100, "hostel": 30, "airbnb": 60, "comida": 35, "transporte": 25
    })
    
    hospedagem = custos.get(tipo_hospedagem, custos["hotel"])
    total_hospedagem = hospedagem * dias
    total_comida = custos["comida"] * dias
    total_transporte = custos["transporte"] * dias
    total = total_hospedagem + total_comida + total_transporte
    
    return {
        "destino": destino,
        "dias": dias,
        "tipo_hospedagem": tipo_hospedagem,
        "hospedagem": total_hospedagem,
        "comida": total_comida,
        "transporte": total_transporte,
        "total": total
    }


def buscar_atracoes(destino: str) -> list:
    """
    Simula busca de atrações turísticas de um destino.
    
    Args:
        destino: Nome da cidade
        
    Returns:
        Lista de atrações
    """
    atracoes = {
        "paris": [
            "Torre Eiffel",
            "Museu do Louvre",
            "Arco do Triunfo",
            "Notre-Dame",
            "Champs-Élysées"
        ],
        "tokyo": [
            "Templo Senso-ji",
            "Torre de Tóquio",
            "Palácio Imperial",
            "Shibuya Crossing",
            "Mercado de Tsukiji"
        ],
        "nova york": [
            "Estatua da Liberdade",
            "Central Park",
            "Times Square",
            "Empire State Building",
            "Brooklyn Bridge"
        ],
        "rio de janeiro": [
            "Cristo Redentor",
            "Pão de Açúcar",
            "Praia de Copacabana",
            "Jardim Botânico",
            "Escadaria Selarón"
        ],
        "londres": [
            "Big Ben",
            "London Eye",
            "Torre de Londres",
            "British Museum",
            "Hyde Park"
        ]
    }
    
    destino_lower = destino.lower()
    return atracoes.get(destino_lower, [
        "Atrações históricas",
        "Museus locais",
        "Parques e jardins",
        "Centro histórico"
    ])


def verificar_visto(destino: str, nacionalidade: str = "brasileira") -> str:
    """
    Simula verificação de necessidade de visto.
    
    Args:
        destino: Nome do país/cidade
        nacionalidade: Nacionalidade do viajante
        
    Returns:
        String com informações sobre visto
    """
    # Simulação simples
    destinos_sem_visto = ["paris", "londres", "rio de janeiro"]
    destinos_com_visto = ["tokyo", "nova york"]
    
    destino_lower = destino.lower()
    
    if destino_lower in destinos_sem_visto:
        return f"Para {destino}: Não é necessário visto para brasileiros (até 90 dias)"
    elif destino_lower in destinos_com_visto:
        return f"Para {destino}: É necessário visto. Consulte o consulado."
    else:
        return f"Para {destino}: Verifique no consulado a necessidade de visto."
