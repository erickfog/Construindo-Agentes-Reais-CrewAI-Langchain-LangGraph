"""
Exemplo de Agente de Planejamento de Viagem usando LangGraph

LangGraph permite criar fluxos de trabalho complexos com controle de estado.
Ideal para processos que precisam de múltiplas etapas bem definidas.

Arquitetura:
- State: Define o estado compartilhado entre os nós
- Nodes: Funções que executam ações específicas
- Edges: Define o fluxo entre os nós
- Graph: Orquestra todo o fluxo
"""

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from tools import consultar_clima, calcular_orcamento, buscar_atracoes, verificar_visto
from typing import TypedDict, List
import os
from dotenv import load_dotenv

load_dotenv()

# Definindo o estado do grafo
class EstadoPlanejamento(TypedDict):
    destino: str
    dias: int
    clima: str
    atracoes: List[str]
    visto: str
    orcamento: dict
    plano_final: str
    etapa_atual: str


# Configurando o modelo LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)


# Definindo os nós (etapas do processo)
def pesquisar_clima(estado: EstadoPlanejamento) -> EstadoPlanejamento:
    """Nó 1: Pesquisa informações sobre o clima"""
    print("🌤️  Pesquisando clima...")
    clima = consultar_clima(estado["destino"], "2024-06-01")
    estado["clima"] = clima
    estado["etapa_atual"] = "clima_pesquisado"
    return estado


def pesquisar_atracoes(estado: EstadoPlanejamento) -> EstadoPlanejamento:
    """Nó 2: Busca atrações turísticas"""
    print("🎯 Buscando atrações...")
    atracoes = buscar_atracoes(estado["destino"])
    estado["atracoes"] = atracoes
    estado["etapa_atual"] = "atracoes_encontradas"
    return estado


def verificar_requisitos_visto(estado: EstadoPlanejamento) -> EstadoPlanejamento:
    """Nó 3: Verifica requisitos de visto"""
    print("📋 Verificando visto...")
    visto = verificar_visto(estado["destino"])
    estado["visto"] = visto
    estado["etapa_atual"] = "visto_verificado"
    return estado


def calcular_orcamento_viagem(estado: EstadoPlanejamento) -> EstadoPlanejamento:
    """Nó 4: Calcula o orçamento"""
    print("💰 Calculando orçamento...")
    orcamento = calcular_orcamento(estado["destino"], estado["dias"])
    estado["orcamento"] = orcamento
    estado["etapa_atual"] = "orcamento_calculado"
    return estado


def criar_plano_final(estado: EstadoPlanejamento) -> EstadoPlanejamento:
    """Nó 5: Cria o plano final usando LLM"""
    print("📝 Criando plano final...")
    
    prompt = f"""Com base nas seguintes informações, crie um plano de viagem completo e organizado:

Destino: {estado['destino']}
Duração: {estado['dias']} dias
Clima: {estado['clima']}
Atrações: {', '.join(estado['atracoes'])}
Visto: {estado['visto']}
Orçamento: R$ {estado['orcamento']['total']:.2f}
  - Hospedagem: R$ {estado['orcamento']['hospedagem']:.2f}
  - Comida: R$ {estado['orcamento']['comida']:.2f}
  - Transporte: R$ {estado['orcamento']['transporte']:.2f}

Crie um plano detalhado incluindo:
1. Resumo da viagem
2. Roteiro diário com atrações
3. Recomendações práticas
4. Informações importantes sobre visto e clima"""
    
    mensagens = [
        SystemMessage(content="Você é um especialista em planejamento de viagens."),
        HumanMessage(content=prompt)
    ]
    
    resposta = llm.invoke(mensagens)
    estado["plano_final"] = resposta.content
    estado["etapa_atual"] = "plano_completo"
    return estado


# Criando o grafo
def criar_grafo_planejamento():
    """Cria e retorna o grafo de planejamento"""
    grafo = StateGraph(EstadoPlanejamento)
    
    # Adicionando nós
    grafo.add_node("pesquisar_clima", pesquisar_clima)
    grafo.add_node("pesquisar_atracoes", pesquisar_atracoes)
    grafo.add_node("verificar_visto", verificar_requisitos_visto)
    grafo.add_node("calcular_orcamento", calcular_orcamento_viagem)
    grafo.add_node("criar_plano", criar_plano_final)
    
    # Definindo o fluxo (edges)
    grafo.set_entry_point("pesquisar_clima")
    grafo.add_edge("pesquisar_clima", "pesquisar_atracoes")
    grafo.add_edge("pesquisar_atracoes", "verificar_visto")
    grafo.add_edge("verificar_visto", "calcular_orcamento")
    grafo.add_edge("calcular_orcamento", "criar_plano")
    grafo.add_edge("criar_plano", END)
    
    return grafo.compile()


def planejar_viagem_langgraph(destino: str, dias: int):
    """
    Função principal para planejar uma viagem usando LangGraph.
    
    Args:
        destino: Nome do destino
        dias: Número de dias da viagem
    """
    print(f"\n{'='*60}")
    print(f"PLANEJANDO VIAGEM COM LANGGRAPH")
    print(f"{'='*60}\n")
    
    # Criando o grafo
    grafo = criar_grafo_planejamento()
    
    # Estado inicial
    estado_inicial = {
        "destino": destino,
        "dias": dias,
        "clima": "",
        "atracoes": [],
        "visto": "",
        "orcamento": {},
        "plano_final": "",
        "etapa_atual": "inicio"
    }
    
    # Executando o grafo
    resultado = grafo.invoke(estado_inicial)
    
    print(f"\n{'='*60}")
    print("RESULTADO FINAL:")
    print(f"{'='*60}")
    print(resultado["plano_final"])
    
    return resultado


if __name__ == "__main__":
    # Exemplo de uso
    planejar_viagem_langgraph("Paris", 5)
